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

import sys
from gi.repository import Gio, GLib

class KeyboardInput:

    def __init__(self, controller):
        self._app_name = "CocoRicoFM"
        self._headless = controller.headless
        self._controller = controller

        if self._headless or sys.platform == "darwin":
            return

        # TODO: port this to asyncio.
        bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        self.proxy = Gio.DBusProxy.new_sync(bus, 0, None, "org.gnome.SettingsDaemon",
                                            "/org/gnome/SettingsDaemon/MediaKeys",
                                            "org.gnome.SettingsDaemon.MediaKeys", None)

        self.grab_keys()

        def on_signal(proxy, sender_name, signal_name, parameters):
            if signal_name == "MediaPlayerKeyPressed":
                self._key_pressed(*parameters)

        self.proxy.connect("g-signal", on_signal)

    def _key_pressed(self, app, key):
        if app != self._app_name:
            return

        if key == "Play":
            self._controller.player.toggle_play()
        elif key == "Stop":
            self._controller.player.stop()
        elif key == "Next":
            # Too bad we don't have access to the Mute key...
            self._controller.player.toggle_mute()

    def grab_keys(self):
        if self._headless or sys.platform == "darwin":
            return

        variant_args = GLib.Variant("(su)", (self._app_name, 0))
        try:
            result = self.proxy.call_sync("GrabMediaPlayerKeys", variant_args, 0, -1, None)
        except:
            pass
