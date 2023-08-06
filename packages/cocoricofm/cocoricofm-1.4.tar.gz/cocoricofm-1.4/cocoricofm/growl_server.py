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
import binascii
import hashlib
import sys

class GrowlPacket:
    def __init__(self, payload):
        self.payload = payload.split(b"\r\n")
        header = self.payload[0].split(b" ")
        self.command_type = header[1]
        # TODO: support for encryption IV (header[2])
        self._auth = header[3]
        self.parsed_message = {}
        for line in self.payload[1:-2]:
            if not line:
                continue
            key_val = line.split(b":")
            self.parsed_message[key_val[0]] = key_val[1].strip()

    def check_password(self, password):
        hash_algo, hashs = self._auth.split(b":")
        ok = False
        # TODO: support for SHA1 and SHA256
        if hash_algo == b"MD5":
            expected_key, salt = hashs.split(b".")
            expected_key = expected_key.decode("utf-8")
            key = hashlib.md5(password.encode("utf-8") + binascii.unhexlify(salt)).digest()
            key_hash = hashlib.md5(key).hexdigest()
            if expected_key == key_hash.upper():
                ok = True
        else:
            print("Unsupported hash algorithm: %s" % hash_algo)
        return ok

class GrowlServerClientProtocol(asyncio.Protocol):
    def __init__(self, password):
        self.password = password

    def connection_made(self, transport):
        self.transport = transport

    async def show_notification(self, title, text):
        p = await asyncio.create_subprocess_exec(sys.executable, '-u', '-m', 'cocoricofm.linux_notify', '%s' % title, '%s' % text)
        return await p.wait()

    def data_received(self, data):
        p = GrowlPacket(data)

        if not p.check_password(self.password):
            reply = b"GNTP/1.0 -ERROR NONE\r\nError-Code: 400\r\nError-Description: NOT_AUTHORIZED\r\n\r\n"
        else:
            if p.command_type == b"NOTIFY":
                headers = p.parsed_message
                title = headers[b"Notification-Title"].decode("utf-8")
                text = headers[b"Notification-Text"].decode("utf-8")
                print("Notify: %s - %s" % (title, text))
                asyncio.ensure_future(self.show_notification(title, text))
            reply = b"GNTP/1.0 -OK NONE\r\n\r\n"

        # FIXME: Workaround for gntp client expecting to receive 1024 bytes from the server...
        padding = 1024 - len(reply)
        reply += b'f' * padding + b"\r\n\r\n"

        self.transport.write(reply)
        self.transport.close()

if __name__ == '__main__':
    import sys

    loop = asyncio.get_event_loop()
    # FIXME: passing password on command-line isn't great
    password = sys.argv[1]
    address = ""
    coro = loop.create_server(lambda: GrowlServerClientProtocol(password), address, 23053)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        server.close()

    loop.run_until_complete(server.wait_closed())
    loop.close()
