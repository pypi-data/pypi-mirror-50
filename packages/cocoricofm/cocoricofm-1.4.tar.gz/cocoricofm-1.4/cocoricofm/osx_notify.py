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
if sys.platform != 'darwin':
    raise ImportError

import asyncio
import Foundation

class Delegate(Foundation.NSObject):

    def userNotificationCenter_shouldPresentNotification_(self, center, notification):
        return True

    def userNotificationCenter_didDeliverNotification_(self, center, notification):

        async def wait_and_remove():
            await asyncio.sleep(5)
            center.removeDeliveredNotification_(notification)
            try:
                self.future.set_result(True)
            except:
                pass

        try:
            self.future.result()
        except:
            asyncio.ensure_future(wait_and_remove())
        else:
            center.removeDeliveredNotification_(notification)

class Notification:

    def __init__(self, app_name, closed_cb=None):
        self.app_name = app_name
        self.actions = []
        self.icon_name = ""
        self.summary = ""
        self.body = ""
        self.centre = Foundation.NSUserNotificationCenter.defaultUserNotificationCenter()
        self.delegate = Delegate.alloc().init()
        self.centre.setDelegate_(self.delegate)

    async def show(self):
        note = Foundation.NSUserNotification.alloc().init()
        note.setIdentifier_(self.app_name)
        note.setTitle_(self.summary)
        note.setInformativeText_(self.body)
        now = Foundation.NSDate.dateWithTimeInterval_sinceDate_(0, Foundation.NSDate.date())
        note.setDeliveryDate_(now)
        self.delegate.future = asyncio.Future()
        self.centre.scheduleNotification_(note)
        return await self.delegate.future

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
    import gbulb
    gbulb.install(False)

    n = Notification('app')

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
