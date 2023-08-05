#!/usr/bin/env python3

# WatchGhost, your invisible but loud monitoring pet
# Copyright © 2015 Kozea

import argparse
import logging
import os
import signal
import sys

from aiohttp.web import run_app
from watchghost import app, config, web  # noqa


def reload_watchghost(signum, frame):  # noqa
    """ Restart WatchGhost on SIGHUP to reload configuration (and files) """
    log = logging.getLogger('watchghost')
    log.info('Signal {} received - reloading WatchGhost'.format(signum))
    try:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except OSError:
        log.error('Error during WatchGhost restart')


def main():
    log = logging.getLogger('watchghost')

    parser = argparse.ArgumentParser(
        description='Your invisible but loud monitoring pet'
    )
    default_config_dir = os.path.expanduser('~/.config/watchghost')
    parser.add_argument(
        '--config',
        dest='config_dir',
        default=default_config_dir,
        help='path to the configuration directory'
    )
    args = parser.parse_args()

    config.read(args.config_dir)
    app.add_routes(web.routes)

    signal.signal(signal.SIGHUP, reload_watchghost)

    log.debug('Listening to http://%s:%i' % ('localhost', 8888))
    run_app(app, host='localhost', port=8888)


if __name__ == '__main__':
    main()
