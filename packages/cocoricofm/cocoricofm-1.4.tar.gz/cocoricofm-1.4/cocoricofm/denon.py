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

class DenonRemote:

    def __init__(self, address):
        self.address = address

    @property
    def enabled(self):
        return self.address != None

    async def _connect(self):
        if not self.enabled:
            fut = asyncio.Future()
            fut.set_result((None, None))
            return await fut

        return await asyncio.open_connection(self.address, 23)

    async def send_command(self, cmd, reader, writer):
        payload = "%s\r" % cmd
        writer.write(payload.encode('ascii'))
        await writer.drain()
        return await reader.readuntil(b'\r')

    async def power_on(self, reader, writer):
        return await self.send_command("PWON", reader, writer)

    async def power_off(self, reader, writer):
        return await self.send_command("PWSTANDBY", reader, writer)

    async def toggle_power(self):
        fut = asyncio.Future()
        reader, writer = await self._connect()
        status = await self.send_command("PW?", reader, writer)
        if status.startswith(b"PWON"):
            await self.power_off(reader, writer)
            powered = False
        else:
            await self.power_on(reader, writer)
            powered = True

        fut.set_result(powered)
        writer.close()
        return await fut

if __name__ == '__main__':
    import sys
    import gbulb
    gbulb.install(False)

    d = DenonRemote(sys.argv[1])

    async def main():
        status = await d.toggle_power()
        print(status)
        await asyncio.sleep(1)
        status = await d.toggle_power()
        print(status)

    f = asyncio.ensure_future(main())
    loop = gbulb.get_event_loop()
    loop.run_until_complete(f)
