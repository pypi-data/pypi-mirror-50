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

import asyncio

try:
    import lirc
except ImportError:
    lirc = None

class LircInput:

    def __init__(self, config, controller):
        if not lirc:
            return

        self._remote_enabled = True
        self._controller = controller
        rc_file = config.get("lirc", "keymap")
        self.socket = lirc.init('cocoricofm', rc_file)

    def reader(self):
        code = lirc.nextcode()
        if code:
            self._handle_input(code[0])

    async def start(self):
        future = asyncio.Future()
        if not lirc:
            future.set_result(False)
            return await future

        loop = asyncio.get_event_loop()
        loop.add_reader(self.socket, self.reader)
        future.set_result(True)
        return await future

    async def _toggle_power(self):
        if self._controller.denon_remote.enabled:
            powered = await self._controller.denon_remote.toggle_power()
            if powered:
                self._controller.player.start()
            else:
                self._controller.player.stop()
        else:
            self._controller.player.toggle_play()

    def _handle_input(self, code):
        if not self._remote_enabled and code != "red":
            return

        if code.startswith("key_"):
            idx = int(code[4:])
            self._controller.tune(idx - 1)
        elif code == "left":
            idx = self._controller.current_station_index()
            self._controller.tune(idx - 1)
        elif code == "right":
            idx = self._controller.current_station_index()
            self._controller.tune(idx + 1)
        elif code in ("pause", "play"):
            self._controller.player.toggle_play()
        elif code == "stop":
            self._controller.player.stop()
        elif code == "increment_volume":
            self._controller.player.increment_volume()
        elif code == "decrement_volume":
            self._controller.player.decrement_volume()
        elif code == "mute":
            self._controller.player.toggle_mute()
        elif code == "record":
            self._controller.player.toggle_recording()
        elif code == "power":
            asyncio.ensure_future(self._toggle_power())
        elif code == "red":
            if self._remote_enabled:
                self._controller.player.stop()
            else:
                self._controller.player.start()
            self._remote_enabled = not self._remote_enabled
        else:
            print("Unhandled input: %s" % code)
