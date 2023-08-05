# WatchGhost, your invisible but loud monitoring pet
# Copyright © 2015 Kozea

import asyncio
import hashlib
import json
import logging
from collections import deque
from datetime import datetime, timedelta, timezone
from random import random

from . import app
from .web import watcher_encoder, watcher_to_dict

logger = logging.getLogger(__name__)


class Config(dict):
    def __getattr__(self, name):
        return self[name]


class Watcher:

    def __init__(self, server, service, config, loggers):
        key = str(config) + (server.name if server else '')
        self.uuid = hashlib.sha224(key.encode()).hexdigest()
        self.server = server
        self.service = service
        self.loggers = loggers

        if server:
            self.server.watchers.append(self)

        self.config = Config(**self.service.config)
        self.config.update(config)

        self.check_results = deque(maxlen=max(1, self.config['retry'] + 1))
        self.is_first_hard = None
        self.hard_check_results = deque(maxlen=2)

        self.description = self.config['description']

        self.plan_next_check()

    @property
    def previous_hard_status(self):
        if len(self.hard_check_results) == 2:
            return self.hard_check_results[-1]['status']
        return None

    @property
    def last_check_result(self):
        if len(self.check_results) > 0:
            return self.check_results[0]
        return None

    @property
    def response(self):
        return self.last_check_result['response']

    @property
    def previous_check_result(self):
        if len(self.check_results) > 1:
            return self.check_results[1]
        return None

    @property
    def status(self):
        lcr = self.last_check_result
        if lcr:
            return lcr['status']
        return None

    @property
    def previous_status(self):
        pcr = self.previous_check_result
        if pcr:
            return pcr['status']
        return None

    @property
    def is_hard(self):
        lcr = self.last_check_result
        return lcr and lcr['is_hard']

    @property
    def previous_is_hard(self):
        pcr = self.previous_check_result
        return pcr and pcr['is_hard']

    @property
    def last_check_start(self):
        lcr = self.last_check_result
        if lcr:
            return lcr['start']
        return None

    def is_in_checking_period(self):
        before = self.config['before']
        after = self.config['after']
        current_time = datetime.now().time()
        return after < current_time < before

    @property
    def next_check_hour(self):
        after = self.config['after']
        now = datetime.now(timezone.utc)

        # if we are in the checking period
        if self.is_in_checking_period():
            # if it is our first check
            if self.last_check_start is None:
                # return "check now"
                return now
            # if it is not our first check
            seconds_from_last_check = (
                (now - self.last_check_start).total_seconds()
            )
            repeat = self.config['repeat']
            # if last check was longer than our repeat frequency
            if seconds_from_last_check > repeat:
                # return "recheck now"
                return now
            # return "wait until then next check hour"
            return now + timedelta(seconds=repeat - seconds_from_last_check)

        # wait until the next checking period
        today_after = datetime.combine(now.date(), after)
        today_after = today_after.replace(tzinfo=timezone.utc)
        if now < today_after:
            return today_after
        tomorrow_after = today_after + timedelta(days=1)
        return tomorrow_after

    @property
    def next_waiting_time(self):
        after = self.config['after']
        now = datetime.now()

        # if we are in the checking period
        if self.is_in_checking_period():
            # if it is our first check
            if self.last_check_start is None:
                # return "check now"
                return 0
            # if it is not our first check
            seconds_from_last_check = (
                (now - self.last_check_start).total_seconds()
            )
            repeat = self.config['repeat']
            # if last check was longer than our repeat frequency
            if seconds_from_last_check > repeat:
                # return "recheck now"
                return 0
            # return "wait until then next check hour"
            return repeat - seconds_from_last_check

        # wait until the next checking period
        today_after = datetime.combine(now.date(), after)
        if now < today_after:
            return (today_after - now).total_seconds()
        tomorrow_after = today_after + timedelta(days=1)
        return (tomorrow_after - now).total_seconds()

    def plan_next_check(self, now=False):
        delta = self.next_check_hour - datetime.now(timezone.utc)
        next_waiting_time = max(0, delta.total_seconds())
        if self.last_check_start is None and self.is_in_checking_period():
            next_waiting_time = random() * 60
        if now:
            next_waiting_time = 0

        loop = asyncio.get_event_loop()
        loop.call_later(
            next_waiting_time, lambda: loop.create_task(self.check())
        )

    def add_check_result(self, response, status, start, end):
        first_index = self.check_results.maxlen
        not_first_statuses = (
            [cr['status'] for cr in self.check_results][0:first_index - 1]
        )
        all_statuses = not_first_statuses + [status]
        is_hard = (
            len(set(all_statuses)) == 1 and
            self.check_results.maxlen == len(all_statuses)
        )
        if is_hard and self.is_first_hard:
            self.is_first_hard = False
        if is_hard and self.is_first_hard is None:
            self.is_first_hard = True

        result = dict(
            response=response,
            start=start,
            end=end,
            status=status,
            is_hard=is_hard,
        )
        self.check_results.appendleft(result)
        if is_hard:
            self.hard_check_results.appendleft(result)

    async def service_check(self):
        start = datetime.now(timezone.utc)
        response = await self.service.check(self.server, self.config)
        end = datetime.now(timezone.utc)
        for status, tests in self.config['status'].items():
            for test in tests:
                for key, value in test.items():
                    if response.get(key) != value:
                        # One of the conditions failed in this test
                        break
                else:
                    # All the conditions are verified for this test
                    break
            else:
                # No test have all conditions verified, try the next status
                continue
            # Current test passes all conditions: keep current status
            break
        else:
            # No test have been found with all condition verified
            logger.warning(
                "{} - incorrect response '{}'.".format(
                    self.service.name, response))
            status = 'unknown'
        return (response, status, start, end)

    async def log(self):
        for logger in self.loggers:
            if logger.should_log(self):
                await logger.log(self)
        for websocket in app.websockets:
            await websocket.send_json({
                self.uuid: json.dumps(
                    watcher_to_dict(self), default=watcher_encoder
                )
            })

    async def check(self, retry=0, replan=True):
        try:
            response, status, start, end = await self.service_check()
            self.add_check_result(response, status, start, end)
            await self.log()
        except Exception:
            logger.exception('')
            status = 'unknown'
        finally:
            # TODO: we should rely on a configuration key
            retry_status = ['warning', 'error', 'critical', 'unknown']
            if status in retry_status and retry < self.config['retry']:
                await asyncio.sleep(self.config['retry_interval'])
                await self.check(retry + 1)
            elif replan:
                self.plan_next_check()
