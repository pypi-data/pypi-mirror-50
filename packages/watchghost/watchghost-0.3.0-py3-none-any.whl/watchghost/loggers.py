# WatchGhost, your invisible but loud monitoring pet
# Copyright © 2015 Kozea

import logging
import smtplib
import socket
import ssl
from email.mime.text import MIMEText
from subprocess import PIPE, Popen
from urllib.parse import urlencode, urlparse

import aiohttp
from influxdb import InfluxDBClient

from .services.network import SSLContext, TCPConnector

logger = logging.getLogger(__name__)


class Logger:
    """
    A logger make a recording of services watches.

    All loggers share the following properties:

    - type: the name of the class to use as logger. This class must be found
      in watchghost.loggers module.
    - status: a list of status level that the logger accepts. A status
      level is one of ``info``, ``warning``, ``error``, ``critical`` or
      ``unknown``.
    - only_hard: whether or not the logger should act only on hard statuses or
      not. A status is hard when a watcher gives the same result N times (N
      being defined on the watcher).

    Example:

    .. code-block:: toml

      [console]
      type = "Console"
      status = ["error", "critical"]
      only_hard = True

    This example defines a logger that will use the class
    ``watchghost.loggers.Console``. This logger will only log ``error`` and
    ``critical`` statuses when these statuses are hard.
    """

    config = {
        'status': None,
        'only_hard': False,
        'only_changes': True,
    }

    @classmethod
    def create(cls, config):
        instance = globals()[config['type']]()
        for key, value in cls.config.items():
            if key not in instance.config:
                instance.config[key] = value
        instance.config.update(config)
        return instance

    def should_log(self, watcher):
        status = self.config['status']
        only_hard = self.config['only_hard']
        only_changes = self.config['only_changes']

        # The status level is enabled for this logger
        status_enabled = (status is None or watcher.status in status)

        # the status changed and the previous status is defined
        status_changed = (
            watcher.status != watcher.previous_status and
            watcher.previous_status is not None
        )

        # the previous status is not info and we are at startup
        status_not_good_at_startup = (
            watcher.status != 'info' and
            watcher.previous_status is None
        )

        # status just changed to be hard
        is_hard_changed = (
            watcher.is_hard and not watcher.previous_is_hard and (
                watcher.status != 'info' or not watcher.is_first_hard
            ) and watcher.status != watcher.previous_hard_status
        )

        if status_enabled:
            if only_hard:
                if only_changes:
                    return is_hard_changed
                else:
                    return watcher.is_hard
            else:
                if only_changes:
                    return status_changed or status_not_good_at_startup
                else:
                    return True
        else:
            return False


class Console(Logger):
    config = {
        'message': (
            '{watcher.description} on {watcher.server.name} '
            '({watcher.last_check_result})'),
        'filename': None,
    }

    async def log(self, watcher):
        if not hasattr(self, 'console_logger'):
            self.console_logger = logging.getLogger('watchghost.console')
            self.console_logger.setLevel('DEBUG')

        if not hasattr(self, 'filename'):
            self.filename = self.config['filename']
            if self.filename:
                handler = logging.handlers.WatchedFileHandler(self.filename)
                self.console_logger.addHandler(handler)

        self.console_logger.log(
            getattr(logging, watcher.status.upper(), logging.ERROR),
            self.config['message'].format(watcher=watcher))


class Sendmail(Logger):
    config = {
        'status': ['warning', 'error', 'critical', 'unknown'],
        'from': 'no-reply@example.com',
        'to': 'no-reply@example.com',
        'subject': 'Error for {watcher.description} on {watcher.server.name}',
        'message': (
            'Error for {watcher.description} on {watcher.server.name}.\n\n'
            '{watcher.last_check_result}')
    }

    async def log(self, watcher):
        message = MIMEText(self.config['message'].format(watcher=watcher))
        message['From'] = self.config['from']
        message['To'] = self.config['to']
        message['Subject'] = self.config['subject'].format(watcher=watcher)
        message['Content-Type'] = 'text/plain; charset="UTF-8"'
        popen = Popen(['/usr/sbin/sendmail', '-t', '-oi'], stdin=PIPE)
        popen.communicate(message.as_string().encode('utf-8'))


class Smtp(Logger):
    config = {
        'status': ['info', 'warning', 'error', 'critical', 'unknown'],
        'from': 'no-reply@example.com',
        'to': 'no-reply@example.com',
        'subject': (
            '{watcher.status} for {watcher.description} on '
            '{watcher.server.name}'
        ),
        'message': (
            '{watcher.status} for {watcher.description} on '
            '{watcher.server.name}.\n\n{watcher.last_check_result}'
        ),
        'smtp_host': 'localhost',
        'smtp_port': 587,
        'smtp_starttls': True,
        'smtp_username': None,
        'smtp_password': None,
    }

    async def log(self, watcher):
        message = MIMEText(self.config['message'].format(watcher=watcher))
        message['From'] = self.config['from']
        message['To'] = self.config['to']
        message['Subject'] = self.config['subject'].format(watcher=watcher)
        message['Content-Type'] = 'text/plain; charset="UTF-8"'
        host = self.config['smtp_host']
        port = self.config['smtp_port']
        with smtplib.SMTP(host, port) as smtp_client:
            if self.config['smtp_starttls']:
                smtp_client.starttls()
            if self.config['smtp_username'] or self.config['smtp_password']:
                smtp_client.login(
                    self.config['smtp_username'],
                    self.config['smtp_password']
                )
            smtp_client.send_message(message)


class SmsOVH(Logger):
    """Docs : http://guides.ovh.com/Http2Sms"""
    config = {
        'status': ['info', 'warning', 'error', 'critical', 'unknown'],
        'base_url': "https://www.ovh.com/cgi-bin/sms/http2sms.cgi?",
        'sms_account': None,
        'sms_login': None,
        'sms_password': None,
        'sms_from': None,
        'sms_to': None,
        'timeout': False,
        'message': (
            "[{watcher.server.name}]"
            " '{watcher.status}' status for '{watcher.description}'")
    }

    async def log(self, watcher):
        params = urlencode({
            'account': self.config['sms_account'],
            'login': self.config['sms_login'],
            'password': self.config['sms_password'],
            'from': self.config['sms_from'],
            'to': self.config['sms_to'],
            'message': self.config['message'].format(watcher=watcher),
            'noStop': '1',
        })
        url = "%s%s" % (self.config['base_url'], params)

        url_parts = urlparse(url)
        hostname = url_parts.hostname

        if url_parts.scheme == 'https':
            context = SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.hostname = hostname
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            context.load_default_certs()
        else:
            context = None

        timeout = aiohttp.ClientTimeout(total=self.config['timeout'])

        try:
            kwargs = dict(timeout=timeout, connector=TCPConnector())
            async with aiohttp.ClientSession(**kwargs) as session:
                response = await session.get(url, ssl=context)

            if response.status != 200:
                logger.error(
                    "'Error when trying to send message via SMS."
                    " Status : %s ; Reason : %s.\nRequest : %s" % (
                        response.code, response.reason, url))
            else:
                body = response.text()
                if len(body) < 2 or body[:2] != 'OK':
                    logger.error(
                        "Error raised when logging message by SMS.\n%s" % (
                            body))

        except socket.timeout:
            logger.exception(
                "Timeout reached (%d) to log message by SMS." % (
                    self.config['timeout']))
        except Exception as e:
            logger.exception(
                "Error raised when logging message by SMS.\n%s" % (e))


class InfluxDB(Logger):
    """Storage of logs in InfluxDB."""
    config = {
        'host': 'localhost',
        'port': 8086,
        'username': 'root',
        'password': 'root',
        'database': 'watchghost',
        'only_changes': False,
    }

    def __init__(self):
        super().__init__()

        self._client = InfluxDBClient(
            host=self.config['host'], port=self.config['port'],
            username=self.config['username'], password=self.config['password'],
            database=self.config['database'])

        # Does nothing if already created
        self._client.create_database(self.config['database'])

    async def log(self, watcher):
        # Use watcher's tags as extra InfluxDB tags
        extra_tags = {
            'tag.{}'.format(key.lower()): value
            for key, value in watcher.config.get('tags', {}).items()
        }

        # Use watcher's results and response items as extra InfluxDB fields
        extra_fields = {
            key: (value if isinstance(value, (int, float)) else str(value))
            for key, value in watcher.last_check_result.items()
            if key != 'response' and value is not None
        }
        for key, value in watcher.last_check_result['response'].items():
            if value is not None:
                extra_fields['response.{}'.format(key)] = (
                    value if isinstance(value, (int, float)) else str(value))

        data = [{
            'measurement': watcher.service.name,
            'time': watcher.last_check_result['start'].isoformat(),
            'tags': {
                'tag.status': watcher.status,
                'tag.server': watcher.server.name,
                'tag.name': watcher.description,
                **extra_tags,
            },
            'fields': {
                'status': watcher.status,
                **extra_fields,
            },
        }]

        self._client.write_points(data)
