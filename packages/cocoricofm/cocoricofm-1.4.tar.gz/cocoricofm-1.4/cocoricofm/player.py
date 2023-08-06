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
import time
import gi
import asyncio
import urllib.parse
import logging

from .tagger import Tagger

gi.require_version('Gst', '1.0')
from gi.repository import Gst

Gst.init([])
gi.require_version('GstPbutils', '1.0')
from gi.repository import GstPbutils, GObject, GLib

class Player(GObject.GObject):
    __gsignals__ = { 'suspended': (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
                     'resumed': (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
                     'volume-changed': (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
                     'mute-changed': (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
                     'recording-changed': (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
                     'tags-updated': (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, controller):
        super(Player, self).__init__()
        self._controller = controller
        self._url = None
        self._output_location = controller.output_path
        self.recording = controller.recording
        self._buffering = False
        self._file_sink = None
        self.pipeline = None
        self._signals = {}
        Gst.init([])
        self._playing = False
        self._pending_pads = {}
        self._recording_file_extension = "mp3"
        self._tagger = Tagger()
        self._current_tags = {}

    def get_pipeline_dot_data(self):
        return Gst.debug_bin_to_dot_data(self.pipeline, Gst.DebugGraphDetails.ALL)

    def song_changed(self, previous):
        if not self.recording:
            return

        def save_recording_and_roll(loop):
            self._save_recording(previous, loop)
            self._roll_to_new_file()
            queue = self.pipeline.get_child_by_name("sink-queue")
            queue.sync_state_with_parent()
            self._file_sink.sync_state_with_parent()
            Gst.debug_bin_to_dot_file(self.pipeline, Gst.DebugGraphDetails.ALL, "new-record")

        self.stop_recorder_flow(save_recording_and_roll)

    def _save_recording(self, song_infos, loop):
        queue = self.pipeline.get_child_by_name("sink-queue")
        queue.set_state(Gst.State.READY)
        self._file_sink.send_event(Gst.Event.new_eos())
        self._file_sink.set_state(Gst.State.NULL)
        full_path = os.path.join(self._output_location, self._current_filename)
        new_path = os.path.join(self._output_location, "%s - %s.%s" % (song_infos.artist, song_infos.title, self._recording_file_extension))
        asyncio.ensure_future(self._tagger.write_tags(full_path, new_path, song_infos), loop=loop)

    def _roll_to_new_file(self):
        self._current_filename = "cocoricofm-%d.mp3" % int(time.time())
        self._file_sink.props.location = os.path.join(self._output_location, self._current_filename)

    def _guess_recording_file_extension(self, caps):
        self._recording_file_extension = 'mp3'
        structure = caps.get_structure(0)
        valid, mpegversion = structure.get_int('mpegversion')
        if valid:
            valid, layer = structure.get_int('layer')
            if not valid:
                level = structure.get_string('level')
                if level:
                    self._recording_file_extension = 'aac'
            else:
                self._recording_file_extension = 'mp%d' % layer

    def _plug_decoder(self, caps):
        factories = Gst.ElementFactory.list_get_elements(Gst.ELEMENT_FACTORY_TYPE_DECODER, Gst.Rank.MARGINAL)
        filtered = Gst.ElementFactory.list_filter(factories, caps, Gst.PadDirection.SINK, caps.is_fixed())
        for factory in filtered:
            for template in factory.get_static_pad_templates():
                if template.direction == Gst.PadDirection.SRC:
                    continue
                tmpl_caps = template.get_caps()
                if not caps.is_subset(tmpl_caps):
                    continue
                decoder = factory.create("audio-decoder")
                if not decoder:
                    continue

                self.pipeline.add(decoder)
                dec_queue = self.pipeline.get_child_by_name('decoder-queue')
                if not dec_queue.link(decoder):
                    self.pipeline.remove(decoder)
                    continue

                if self.volume_element:
                    decoder.link(self.volume_element)
                else:
                    decoder.link(self.audio_sink)

                decoder.sync_state_with_parent()
                self._guess_recording_file_extension(caps)
                if self.recording:
                    self.enable_recording()

                return

        if caps.is_fixed():
            bus = self.pipeline.get_bus()
            bus.post(GstPbutils.missing_decoder_message_new(self.pipeline, caps))
        return None

    def _configure_pipeline(self):
        self.pipeline = Gst.Pipeline()
        self.src = Gst.Element.make_from_uri(Gst.URIType.SRC, self._url, "src")
        self.pipeline.add(self.src)

        def caps_notify_cb(pad, param_spec, user_data):
            caps = pad.get_current_caps()
            if caps:
                self._plug_decoder(caps)
                pad.disconnect(self._pending_pads[pad])
                del self._pending_pads[pad]

        def handle_new_parse_pad(parsebin, pad):
            queue = self.pipeline.get_child_by_name("src-queue")
            tee = self.pipeline.get_child_by_name("tee")
            dec_queue = self.pipeline.get_child_by_name('decoder-queue')
            if not queue:
                queue = Gst.ElementFactory.make("queue2", "src-queue")
                queue.props.use_buffering = True
                queue.props.use_tags_bitrate = True

                tee = Gst.ElementFactory.make("tee", "tee")
                dec_queue = Gst.ElementFactory.make("queue", "decoder-queue")
                self.pipeline.add(queue)
                self.pipeline.add(tee)
                self.pipeline.add(dec_queue)

                queue_sink_pad = dec_queue.get_static_pad("sink")
                src_pad = tee.get_request_pad("src_%u")
                src_pad.link(queue_sink_pad)

                queue.link(tee)

            queue_sink_pad = queue.get_static_pad("sink")
            pad.link(queue_sink_pad)

            dec_queue.sync_state_with_parent()
            tee.sync_state_with_parent()
            queue.sync_state_with_parent()

            caps = pad.get_current_caps()
            if caps:
                self._plug_decoder(caps)
            else:
                self._pending_pads[pad] = pad.connect('notify::caps', caps_notify_cb, None)

        def handle_dropped_parse_pad(parsebin, pad):
            decoder = self.pipeline.get_child_by_name("audio-decoder")
            if decoder:
                dec_queue = self.pipeline.get_child_by_name("decoder-queue")
                if self.volume_element:
                    decoder.unlink(self.volume_element)
                else:
                    decoder.unlink(self.audio_sink)
                dec_queue.unlink(decoder)
                decoder.set_state(Gst.State.NULL)
                self.pipeline.remove(decoder)
            queue = self.pipeline.get_child_by_name("src-queue")
            sink_pad = queue.get_static_pad("sink")
            pad.unlink(sink_pad)

        parsebin = Gst.ElementFactory.make("parsebin", "parsebin")
        pad_added_sig = parsebin.connect("pad-added", handle_new_parse_pad)
        pad_removed_sig = parsebin.connect("pad-removed", handle_dropped_parse_pad)
        self._signals['parsebin'] = (pad_added_sig, pad_removed_sig)
        self.pipeline.add(parsebin)

        self.src.link(parsebin)

        self.volume_element = None
        self.audio_sink = Gst.ElementFactory.make("autoaudiosink", "audio-sink")
        self.pipeline.add(self.audio_sink)
        self.audio_sink.set_state(Gst.State.READY)
        self.platform_audio_sink = self.audio_sink.get_child_by_index(0)

        # FIXME: properly check the sink implements the stream volume interface. Somehow.
        if not hasattr(self.platform_audio_sink.props, 'volume') or not hasattr(self.platform_audio_sink.props, 'mute'):
            self.volume_element = Gst.ElementFactory.make("volume", "volume")
            volume_sig = self.volume_element.connect("notify::volume", self._volume_changed_cb)
            mute_sig = self.volume_element.connect("notify::mute", self._mute_changed_cb)
            self._signals['volume'] = (volume_sig, mute_sig)
            self.pipeline.add(self.volume_element)
            self.volume_element.link(self.audio_sink)
        else:
            volume_sig = self.platform_audio_sink.connect("notify::volume", self._volume_changed_cb)
            mute_sig = self.platform_audio_sink.connect("notify::mute", self._mute_changed_cb)
            self._signals['audio-sink'] = (volume_sig, mute_sig)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_gst_message)
        self.pipeline.set_state(Gst.State.READY)

    def set_url(self, url):
        if not url or (url == self._url):
            return

        if not self._url:
            self._url = url
            self._configure_pipeline()
        else:
            previous_url_parsed = urllib.parse.urlparse(self._url)
            next_url_parsed = urllib.parse.urlparse(url)
            self._url = url
            self.pipeline.set_state(Gst.State.NULL)
            if previous_url_parsed.scheme == next_url_parsed.scheme:
                self.src.props.location = self._url
            else:
                parsebin = self.pipeline.get_child_by_name("parsebin")
                self.src.unlink(parsebin)
                self.src.set_state(Gst.State.NULL)
                self.pipeline.remove(self.src)

                self.src = Gst.Element.make_from_uri(Gst.URIType.SRC, self._url, "src")
                self.pipeline.add(self.src)
                self.src.link(parsebin)

        self.start()

    def set_recording_output_location(self, location):
        self._output_location = location

    def enable_recording(self):
        if self.pipeline.get_child_by_name("file-sink"):
            return

        self._file_sink = Gst.ElementFactory.make("filesink", "file-sink")
        self._file_sink.props.sync = True
        sink_queue = Gst.ElementFactory.make("queue", "sink-queue")
        self.pipeline.add(self._file_sink)
        self.pipeline.add(sink_queue)

        self._roll_to_new_file()
        sink_queue.link(self._file_sink)
        sink_queue_sink_pad = sink_queue.get_static_pad("sink")
        tee = self.pipeline.get_child_by_name("tee")
        self.tee_recording_src_pad = tee.get_request_pad("src_%u")
        self.tee_recording_src_pad.link(sink_queue_sink_pad)

        self._file_sink.sync_state_with_parent()
        sink_queue.sync_state_with_parent()
        self.recording = True
        self.dispatch_signal('recording-changed')
        Gst.debug_bin_to_dot_file(self.pipeline, Gst.DebugGraphDetails.ALL, "record-enabled")

    def disable_recording(self):

        def cleanup(loop):
            song_infos = self._controller.current_song_infos
            self._save_recording(song_infos, loop)
            queue = self.pipeline.get_child_by_name("sink-queue")
            queue.set_state(Gst.State.NULL)
            self.pipeline.remove(self._file_sink)
            self.pipeline.remove(queue)
            self._file_sink = None
            tee = self.pipeline.get_child_by_name("tee")
            tee.release_request_pad(self.tee_recording_src_pad)
            self.tee_recording_src_pad = None
            self.recording = False
            self.dispatch_signal('recording-changed')
            Gst.debug_bin_to_dot_file(self.pipeline, Gst.DebugGraphDetails.ALL, "record-disabled")

        self.stop_recorder_flow(cleanup)

    def stop_recorder_flow(self, callback):
        loop = asyncio.get_event_loop()

        def pad_probe_cb(pad, info, user_data):
            if user_data['ok'] == False:
                user_data['ok'] = True
                return Gst.PadProbeReturn.OK

            callback(user_data['loop'])
            return Gst.PadProbeReturn.REMOVE

        async def setup_probe(user_data):
            self.tee_recording_src_pad.add_probe(Gst.PadProbeType.IDLE, pad_probe_cb, user_data)

        user_data = {'ok': False, 'loop': loop}
        asyncio.ensure_future(setup_probe(user_data), loop=loop)

    def toggle_recording(self):
        if self.recording:
            self.disable_recording()
        else:
            self.enable_recording()

    def dispatch_signal(self, name):
        def dispatch_cb(*args):
            self.emit(name)
            return GLib.SOURCE_REMOVE

        GObject.idle_add(dispatch_cb)

    def _volume_changed_cb(self, playbin, pspec):
        self.dispatch_signal("volume-changed")

    def _mute_changed_cb(self, playbin, pspec):
        self.dispatch_signal("mute-changed")

    @property
    def playing(self):
        return self._playing

    @property
    def volume(self):
        if self.volume_element:
            element = self.volume_element
        else:
            element = self.platform_audio_sink
        return element.props.volume

    @property
    def muted(self):
        if self.volume_element:
            element = self.volume_element
        else:
            element = self.platform_audio_sink
        return element.props.mute

    @property
    def metadata_tags(self):
        return self._current_tags

    def toggle_mute(self):
        if self.volume_element:
            element = self.volume_element
        else:
            element = self.platform_audio_sink
        element.props.mute = not element.props.mute

    def set_volume(self, value):
        if self.volume_element:
            element = self.volume_element
        else:
            element = self.platform_audio_sink
        # Clamp between 0 and 1.
        element.props.volume = max(min(value, 1.), 0.)

    def apply_volume_delta(self, delta):
        if self.volume_element:
            element = self.volume_element
        else:
            element = self.platform_audio_sink
        value = element.props.volume + delta
        self.set_volume(value)

    def increment_volume(self):
        self.apply_volume_delta(0.05)

    def decrement_volume(self):
        self.apply_volume_delta(float(-0.05))

    def _teardown_pipeline(self):
        for elt_name, handlers in self._signals.items():
            element = self.pipeline.get_child_by_name(elt_name)
            for handler in handlers:
                GObject.signal_handler_disconnect(element, handler)
        self._signals = {}
        self.pipeline = None

    def _on_gst_message(self, bus, message):
        if not message:
            return
        t = message.type
        if t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            logging.error("Error: %s (debug: %s)" % (err, debug))
            logging.info("Restarting...")
            self.pipeline.set_state(Gst.State.NULL)
            self._teardown_pipeline()
            self._configure_pipeline()
            self.start()
        elif t == Gst.MessageType.BUFFERING:
            percent = message.parse_buffering()
            result, state, pending = self.pipeline.get_state(0)
            self._buffering = percent < 100
            if state == Gst.State.PLAYING and percent < 100:
                self.pipeline.set_state(Gst.State.PAUSED)
            elif state == Gst.State.PAUSED and percent == 100:
                self.pipeline.set_state(Gst.State.PLAYING)
        elif t == Gst.MessageType.ASYNC_DONE:
            if self.volume_element:
                self.dispatch_signal('volume-changed')
                self.dispatch_signal('mute-changed')
        elif t == Gst.MessageType.STATE_CHANGED:
            if message.src == self.pipeline:
                old, new, pending = message.parse_state_changed()
                if old == Gst.State.PAUSED and new == Gst.State.PLAYING and not self._buffering:
                    self._playing = True
                    self.dispatch_signal("resumed")
        elif t == Gst.MessageType.TAG:
            tag_list = message.parse_tag()
            self._current_tags, old_tags = {}, self._current_tags
            for i in range(tag_list.n_tags()):
                name = tag_list.nth_tag_name(i)
                self._current_tags[name] = tag_list.get_value_index(name, i)
                # TODO: Support for dates?
            if old_tags and (old_tags != self._current_tags):
                self.dispatch_signal("tags-updated")

    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self, *args, emit_signal=True, **kwargs):
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)
        self._playing = False
        if emit_signal:
            self.dispatch_signal("suspended")

    def toggle_stop(self):
        if not self._playing:
            self.start()
        else:
            self.stop()

    def toggle_play(self):
        result, state, pending = self.pipeline.get_state(0)
        if state == Gst.State.PLAYING:
            new_state = Gst.State.PAUSED
            self.dispatch_signal("suspended")
        else:
            new_state = Gst.State.PLAYING
            self.dispatch_signal("resumed")
        self.pipeline.set_state(new_state)
