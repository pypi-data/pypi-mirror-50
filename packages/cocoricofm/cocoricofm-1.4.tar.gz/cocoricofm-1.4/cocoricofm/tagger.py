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

import os
import gi
import logging

gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('GstTag', '1.0')
from gi.repository import Gst, GstBase, GstTag, GObject, GLib

class Tagger:
    async def write_tags(self, input_filename, output_filename, song_infos):
        if not output_filename.endswith("mp3"):
            logging.warning("Tagger can write only MP3 for now. Copying recording file as-is.")
            try:
                os.rename(full_path, new_path)
            except FileNotFoundError:
                pass
            return

        self._pipeline = Gst.parse_launch("filesrc name=src location=\"%s\" ! id3mux name=mux ! filesink location=\"%s\"" % (input_filename, output_filename))
        tag_setter = self._pipeline.get_by_interface(Gst.TagSetter)
        if tag_setter and song_infos:
            tags = Gst.TagList.new_empty()
            tags.add_value(Gst.TagMergeMode.APPEND, Gst.TAG_ARTIST, song_infos.artist)
            tags.add_value(Gst.TagMergeMode.APPEND, Gst.TAG_ALBUM, song_infos.album)
            tags.add_value(Gst.TagMergeMode.APPEND, Gst.TAG_TITLE, song_infos.title)
            tags.add_value(Gst.TagMergeMode.APPEND, Gst.TAG_PUBLISHER, song_infos.label)
            if song_infos.year:
                date = GLib.Date.new_dmy(1, 1, song_infos.year)
                tags.add_value(Gst.TagMergeMode.APPEND, Gst.TAG_DATE, date)
            if song_infos.cover_url:
                data = await song_infos.fetch_cover()
                buf = Gst.Buffer.new_wrapped(bytes(data))
                probe_result = GstBase.type_find_helper_for_buffer(None, buf)
                caps = probe_result[0]
                infos = Gst.Structure.new_empty("GstTagImageInfo")
                infos.set_value("image-type", GstTag.TagImageType.FRONT_COVER)
                img_sample = Gst.Sample.new(buf, caps, None, infos)
                #img_sample = GstTag.tag_image_data_to_image_sample(bytes(data), len(data), GstTag.TagImageType.FRONT_COVER)
                tags.add_value(Gst.TagMergeMode.APPEND, Gst.TAG_IMAGE, img_sample)

            current_tags = tag_setter.get_tag_list()
            merge_mode = tag_setter.get_tag_merge_mode()
            tag_setter.merge_tags(tags, merge_mode)

        loop = GObject.MainLoop()
        bus = self._pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.bus_call, loop)

        self._pipeline.set_state(Gst.State.PLAYING)
        try:
            loop.run()
        except:
            pass

        self._pipeline.set_state(Gst.State.NULL)

    def bus_call(self, bus, message, loop):
        t = message.type
        if t == Gst.MessageType.EOS:
            loop.quit()
            src = self._pipeline.get_child_by_name("src")
            os.unlink(src.props.location)
