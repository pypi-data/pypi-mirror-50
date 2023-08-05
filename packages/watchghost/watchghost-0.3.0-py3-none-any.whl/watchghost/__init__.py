# WatchGhost, your invisible but loud monitoring pet
# Copyright © 2015 Kozea

import os

import aiohttp_jinja2
import jinja2
from aiohttp.web import Application

jinja2_loader = jinja2.FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'templates')
)

app = Application()
aiohttp_jinja2.setup(app, loader=jinja2_loader)
app.websockets = []
