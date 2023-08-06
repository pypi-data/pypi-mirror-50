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

# http://pythonhosted.org/gntp/
import gntp.notifier

import uuid
import asyncio

class Notification:

    def __init__(self, app_name, credentials, closed_cb=None):
        self.app_name = app_name
        self.credentials = {}
        self.growls = {}
        self.actions = []
        self.summary = ""
        self.body = ""
        self.icon_name = ""
        self.id = uuid.uuid4().urn
        self.noteType = "Now playing"
        for item in credentials:
            self.credentials[item['hostname']] = item['password']
            self.connect_to(item['hostname'])

    def connect_to(self, hostname):
        password = self.credentials[hostname]
        # TODO: make this async.
        growl = gntp.notifier.GrowlNotifier(self.app_name, hostname=hostname,
                                            password=password,
                                            notifications=[self.noteType,])
        try:
            growl.register()
        except Exception as exc:
            print("Failed to connect to Growl service at %s: %s" % (hostname, str(exc)))
            growl = None
        else:
            self.growls[hostname] = growl
        return growl

    async def show(self):
        future = asyncio.Future()

        async def wait():
            await asyncio.sleep(5)
            future.set_result(True)
            return future

        asyncio.ensure_future(wait())

        if not self.body:
            return await future

        def do_show(growl):
            growl.notify(noteType=self.noteType, title=self.summary, description=self.body,
                         identifier=self.id, sticky=True)

        for hostname in self.credentials.keys():
            if hostname in self.growls.keys():
                growl = self.growls[hostname]
            else:
                growl = self.connect_to(hostname)
            if growl:
                try:
                    do_show(growl)
                except:
                    # Try again.
                    growl = self.connect_to(hostname)
                    if growl:
                        do_show(growl)

        return await future

    async def close(self):
        future = asyncio.Future()
        future.set_result(True)
        return await future

    def update(self, summary, body):
        self.summary = summary
        self.body = body

    def add_action(self, name, label, callback):
        pass

    def clear_actions(self):
        pass

if __name__ == '__main__':
    import sys
    import gbulb
    gbulb.install(False)

    n = Notification('app', [{"hostname": sys.argv[1], "password": sys.argv[2]},])

    async def show1():
        n.update("foo1", "bar1")
        return await n.show()

    async def show2():
        n.update("foo2", "bar2")
        return await n.show()

    async def main():
        await show1()
        await show2()

    f = asyncio.ensure_future(main())
    loop = gbulb.get_event_loop()
    loop.run_until_complete(f)
