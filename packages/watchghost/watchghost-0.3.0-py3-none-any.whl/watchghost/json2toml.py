#!/usr/bin/env python

import argparse
import json
import os
from datetime import time
from os.path import join

import toml


def json_to_toml(source, destination, transform=None):
    with open(source) as f:
        objects = json.loads(f.read())

    if transform:
        objects = transform(objects)
    with open(destination, 'w') as f:
        f.write(toml.dumps(objects))


def watchers_transform(watchers):
    newstruct = {}
    for watcher in watchers:
        watcher_name = (
            watcher['description'] + '_' + (
                watcher.get('host') or watcher.get('group')
                or watcher.get('server')
            )
        )
        assert watcher_name not in newstruct
        if 'after' in watcher:
            watcher['after'] = time.strptime(watcher['after'], '%H:%M:%S')
        if 'before' in watcher:
            watcher['before'] = time.strptime(watcher['before'], '%H:%M:%S')
        newstruct[watcher_name] = watcher
    return newstruct


def loggers_transform(loggers):
    newstruct = {}
    for logger in loggers:
        newstruct[logger['type'].lower()] = logger
    return newstruct


CONFNAME_TRANSFORMS = [
    ('servers', None),
    ('groups', None),
    ('loggers', loggers_transform),
    ('watchers', watchers_transform),
]


def main():
    parser = argparse.ArgumentParser(
        description='Tool to migrate Watchghost conf from JSON to TOML'
    )
    default_config_dir = os.path.expanduser('~/.config/watchghost')
    parser.add_argument(
        '--config',
        dest='config_dir',
        default=default_config_dir,
        help='path to the configuration directory'
    )
    args = parser.parse_args()

    args.config_dir

    for confname, transform in CONFNAME_TRANSFORMS:
        path = join(args.config_dir, confname)
        json_to_toml(path, path + '.toml', transform)
        print('wrote ' + confname + '.toml')


if __name__ == '__main__':
    main()
