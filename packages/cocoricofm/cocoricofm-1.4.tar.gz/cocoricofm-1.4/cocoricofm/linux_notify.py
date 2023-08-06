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

from gi.repository import GLib, Gio
import asyncio
import sys

if sys.platform == 'darwin':
    raise ImportError

class Notification:

    def __init__(self, app_name, closed_cb=None):
        self.app_name = app_name
        self.closed_cb = closed_cb
        self.summary = ""
        self.body = ""
        self.actions = []
        self._actions = {}
        self.icon_name = ""
        self.remote_object = None
        self.id = -1

    async def _connect(self):
        def on_signal(proxy, sender_name, signal_name, parameters):
            params = tuple(parameters)
            if params[0] != self.id:
                return
            if signal_name == "NotificationClosed":
                if self.closed_cb:
                    self.closed_cb(*params[1:])
            elif signal_name == "ActionInvoked":
                callback = self._actions[params[1]]
                callback(self, params[1])

        def proxy_created(proxy, result, future):
            self.remote_object = Gio.DBusProxy.new_finish(result)
            self.remote_object.connect("g-signal", on_signal)
            future.set_result(self.remote_object)

        def connected_cb(unused, result, future):
            bus = Gio.bus_get_finish(result)
            service_name = "org.freedesktop.Notifications"
            object_path = "/org/freedesktop/Notifications"
            interface_name = "org.freedesktop.Notifications"
            Gio.DBusProxy.new(bus, 0, None, service_name, object_path, interface_name, None, proxy_created, future)

        future = asyncio.Future()
        Gio.bus_get(Gio.BusType.SESSION, None, connected_cb, future)
        return await future

    async def show(self):
        if self.id < 0 or not self.remote_object:
            replaces_id = 0
            remote_object = await self._connect()
        else:
            replaces_id = self.id
            remote_object = self.remote_object
        self.hints = {"transient": GLib.Variant("b", True)}
        expire_timeout = 5000
        args = (self.app_name, replaces_id, self.icon_name, self.summary, self.body,
                self.actions, self.hints, expire_timeout)
        variant_args = GLib.Variant("(susssasa{sv}i)", args)

        def call_finished(proxy, task, future):
            result = proxy.call_finish(task)
            try:
                self.id = result[0]
            except IndexError:
                future.set_result(None)
            else:
                future.set_result(self.id)

        future = asyncio.Future()
        remote_object.call("Notify", variant_args, 0, -1, None, call_finished, future)
        return await future

    async def close(self):
        if self.id < 0:
            return
        variant_args = GLib.Variant("(u)", (self.id,))

        def call_finished(proxy, task, future):
            result = proxy.call_finish(task)
            future.set_result(result)

        future = asyncio.Future()
        self.remote_object.call("CloseNotification", variant_args, 0, -1, None, call_finished, future)
        return await future

    def update(self, summary, body):
        self.summary = summary
        self.body = body

    def add_action(self, name, label, callback):
        self._actions[name] = callback
        self.actions.extend([name, label])

    def clear_actions(self):
        self.actions = []
        self._actions = {}

def main(args):
    import gbulb
    gbulb.install()

    if len(args[1:]) != 2:
        print("Usage: %s 'summary' 'body'" % args[0])
        return 1

    summary, body = args[1:]

    loop = asyncio.get_event_loop()

    def closed_cb(reason):
        loop.stop()

    async def close_soon(notification):
        return await notification.close()

    def close(notification):
        f = asyncio.ensure_future(close_soon(notification))
        loop.run(f)

    notification = Notification("CocoRicoFM", closed_cb)

    async def show_notification():
        notification.update(summary, body)
        return await notification.show()

    asyncio.ensure_future(show_notification())
    timer_handle = loop.call_later(15, close, notification)
    loop.run_forever()
    timer_handle.cancel()
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
