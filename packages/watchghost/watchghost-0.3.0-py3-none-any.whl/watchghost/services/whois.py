# WatchGhost, your invisible but loud monitoring pet
# Copyright © 2015 Kozea

from collections import OrderedDict
from datetime import datetime

import whois


class Expire:
    """Probe checking if domain is expired, using JWA services.

    Specific configuration keys:
    - domain: domain to check
    - minimum_days_left_warning: number of days. if the threshold is
      reached, a warning is raised. (28 by default)
    - minimum_days_left_error: number of days. if the threshold is
      reached, an error is raised. (7 by default)
    """

    config = {
        'repeat': 60 * 60 * 24,  # check each day
        'timeout': 5,
        'domain': '',
        'minimum_days_left_warning': 28,
        'minimum_days_left_error': 7,
        'status': OrderedDict([
            ('critical', [
                {'ok': False},
            ]),
            ('error', [
                {"registered": False},
                {"enough_days_left_error": False},
            ]),
            ('warning', [
                {'enough_days_left_warning': False},
            ]),
            ('info', [{}]),
        ]),
    }

    @staticmethod
    async def check(server, config):
        result = {'ok': False}

        try:
            whois_data = whois.whois(config['domain'])
            result.update({
                'message': whois_data,
            })

            expire_date = whois_data.expiration_date
            # In some weird case, the expiration_date is a list of
            # expiration dates. Selecting the worst date
            if type(expire_date) is list:
                expire_date = min(expire_date)

            if expire_date:
                days_left = (expire_date - datetime.now()).days
                result.update({
                    'ok': True,
                    'enough_days_left_error': (
                        days_left > config['minimum_days_left_error']),
                    'enough_days_left_warning': (
                        days_left > config['minimum_days_left_warning'])
                })
        except whois.parser.PywhoisError as e:
            # PywhoisError doesn't have 'message' atttr.
            # Note : This error can be raised if there are too manyu requests
            # in a few time. That makes this watchers not scallable.
            result.update({'message': "PywhoisError: %s" % e.__str__()})
        except ConnectionError:
            result.update({'message': "Unable to establish a connection"})
        return result
