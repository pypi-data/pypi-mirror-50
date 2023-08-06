
import asyncio

import gi
gi.require_version('Soup', '2.4')
from gi.repository import Soup, Gio


class HttpClient:
    def __init__(self):
        self.session = Soup.Session()

    async def get(self, uri, raw=False):
        message = Soup.Message.new("GET", uri)
        f = asyncio.Future()
        self.session.send_async(message, None, self.on_get_finished, {'message': message, 'future': f, 'raw': raw})
        return await f

    def on_get_finished(self, session, result, data):
        message = data['message']
        f = data['future']
        raw = data['raw']
        try:
            input_stream = session.send_finish(result)
        except:
            f.set_result(b"" if raw else "")
            return
        status_code = message.status_code

        if input_stream:
            data_input_stream = Gio.DataInputStream.new(input_stream)
            lines = list()
            if raw:
                while True:
                    if f.cancelled():
                        break
                    payload = data_input_stream.read_bytes(8192, None)
                    if not payload:
                        break
                    if not payload.get_size():
                        break
                    lines.append(payload.get_data())
                result = b"".join(lines)
            else:
                while True:
                    if f.cancelled():
                        break
                    line, length = data_input_stream.read_line_utf8()
                    if not line:
                        break
                    else:
                        lines.append(line)
                result = "\n".join(lines)
            if not f.cancelled():
                f.set_result(result)

    async def post(self, uri, data):
        message = Soup.Message.new("POST", uri)
        message.set_request("application/x-www-form-urlencoded",
                            Soup.MemoryUse.COPY, bytes(data, 'utf-8'))
        f = asyncio.Future()
        self.session.send_async(message, None, self.on_post_finished, {'message': message, 'future': f})
        return await f

    def on_post_finished(self, session, result, data):
        message = data['message']
        f = data['future']
        try:
            input_stream = session.send_finish(result)
        except:
            f.set_result("")
            return

        if input_stream:
            data_input_stream = Gio.DataInputStream.new(input_stream)
            lines = list()
            while True:
                line, length = data_input_stream.read_line_utf8()
                if line is None:
                    break
                else:
                    lines.append(line)
            page = "\n".join(lines)
            f.set_result(page)
