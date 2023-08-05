# WatchGhost, your invisible but loud monitoring pet
# Copyright © 2015 Kozea

import json
import os
from datetime import datetime, time

import aiohttp
import aiohttp_jinja2
from aiohttp import web

from . import app

routes = web.RouteTableDef()
routes.static('/static/', os.path.join(os.path.dirname(__file__), 'static'))


@routes.view('/')
class Index(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        return {}


@routes.view('/api/watchers/{watcher_uuid:[0-9a-f]+}/check_now/')
class CheckNow(web.View):
    async def get(self):
        watcher_uuid = self.request.match_info['watcher_uuid']
        for watchers in app.watchers.values():
            for watcher in watchers:
                if watcher.uuid == watcher_uuid:
                    await watcher.check(replan=False)
                    return
        return


@routes.view('/websocket')
class WebSocket(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        app.websockets.append(ws)
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.ERROR:
                break
        app.websockets.remove(ws)
        return ws


@routes.view('/api/services/')
class ServicesListApi(web.View):
    async def get(self):
        return web.json_response({'objects': [
            dict(service) for service in app.services.values()
        ]})


def watcher_to_dict(w):
    return {
        'uuid': w.uuid,
        'server': dict(w.server) if w.server else {},
        'service': dict(w.service),
        'status': w.status,
        'last_result': w.last_check_result,
        'description': w.description,
        'next_check_hour': w.next_check_hour,
        'tags': w.config.get('tags', {}),
    }


def watcher_encoder(o):
    if isinstance(o, bytes):
        return o.decode()
    if isinstance(o, (datetime, time)):
        return o.isoformat()
    raise TypeError(repr(o) + ' is not json serializable')


def watchers_dumps(*args, **kwargs):
    kwargs['default'] = watcher_encoder
    return json.dumps(*args, **kwargs)


@routes.view('/api/watchers/')
class WatchersListApi(web.View):
    async def get(self):
        return web.json_response({'objects': [
            watcher_to_dict(w) for l in app.watchers.values() for w in l
        ]}, dumps=watchers_dumps)


@routes.view('/api/servers/')
class ServersListApi(web.View):
    async def get(self):
        return web.json_response({'objects': [
            dict(s) for s in app.servers.values()
        ]})


def groups_to_dictlist(groups):
    for name, servers in groups.items():
        yield {'name': name, 'members': [server.uuid for server in servers]}


@routes.view('/api/groups/')
class GroupsListApi(web.View):
    async def get(self):
        return web.json_response({'objects': list(groups_to_dictlist(
            app.groups
        ))})


@routes.view('/api/loggers/')
class LoggersListApi(web.View):
    async def get(self):
        return web.json_response({'objects': [
            {'type': str(type(x)) for x in app.loggers}
        ]})
