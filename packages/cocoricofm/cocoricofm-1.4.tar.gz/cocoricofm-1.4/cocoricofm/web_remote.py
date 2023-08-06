# This file is part of CocoRicoFM.
#
# CocoRicoFM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CocoRicoFM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CocoRicoFM.  If not, see <http://www.gnu.org/licenses/>.

import base64
import os
import pkg_resources
from . import radios
import asyncio
from aiohttp import web
import aiohttp_jinja2
import jinja2

async def tune(request):
    station = request.query['station']
    request.app.radio_controller.tune_station_with_name(station)
    return web.HTTPFound('/')

@aiohttp_jinja2.template('index.html')
async def index(request):
    stations = list(radios.STATIONS.keys())
    stations.sort()
    current_station = request.app.radio_controller.station_name

    song = request.app.radio_controller.previous_status
    if not song:
        song = radios.SongInfos("", "", "", 0)

    cover_data = await song.fetch_cover()
    cover_data = base64.encodebytes(cover_data).replace(b'\n', b'')

    return {'stations': stations, 'song': song, 'cover_data': cover_data.decode(),
            'current_station': current_station}

@aiohttp_jinja2.template('pipeline.html')
async def show_pipeline(request):
    dot_data = request.app.radio_controller.player.get_pipeline_dot_data()
    dot_data = dot_data.replace('"', '\\"')
    dot_data = dot_data.replace('\l', '\n')
    return {'dot_data': dot_data}

async def get_static_file(request):
    name = request.match_info['filename']
    data = pkg_resources.resource_string('cocoricofm', os.path.join('static', name))
    return web.Response(text=data.decode())

class WebRemote:

    def __init__(self, controller):
        self._controller = controller

    async def start(self):
        loop = asyncio.get_event_loop()
        app = web.Application(loop=loop)
        app.radio_controller = self._controller
        aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('cocoricofm', 'templates'))
        app.router.add_route('GET', '/', index)
        app.router.add_route('GET', '/tune/', tune)
        app.router.add_route('GET', '/pipeline', show_pipeline)
        app.router.add_route('GET', '/static/{filename}', get_static_file)
        server = await loop.create_server(app.make_handler(), '0.0.0.0', self._controller.http_port)
        return server
