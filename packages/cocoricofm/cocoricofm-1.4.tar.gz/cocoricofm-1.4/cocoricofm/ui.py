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
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, GObject, Gtk, Gio, GdkPixbuf

from . import radios

class AppWindow(Gtk.ApplicationWindow):
    DEFAULT_WIDTH = 390

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = kwargs["application"]
        self._player = self.app.player
        self._controller = self.app.controller

        self._progress_bar_update_handler = 0
        self._next_song_ts = -1
        self._controller.connect('next-refresh-in', self._reset_progress_bar)
        self._player.connect("suspended", self._player_suspended)
        self._player.connect("resumed", self._player_resumed)
        self._player.connect("volume-changed", self._player_volume_changed)
        self._player.connect("mute-changed", self._player_mute_changed)
        self._player.connect("recording-changed", self._player_recording_changed)

        # This will be in the windows group and have the "win" prefix
        self._record_action = Gio.SimpleAction.new_stateful("record", None,
                                                      GLib.Variant.new_boolean(False))
        self._record_action.connect("change-state", self.toggle_recording)
        self.add_action(self._record_action)

        self._mute_action = Gio.SimpleAction.new_stateful("mute", None,
                                                      GLib.Variant.new_boolean(False))
        self._mute_action.connect("change-state", self.toggle_mute)
        self.add_action(self._mute_action)

        self._stop_action = Gio.SimpleAction.new_stateful("stop", None,
                                                      GLib.Variant.new_boolean(False))
        self._stop_action.connect("change-state", self.toggle_stop)
        self.add_action(self._stop_action)

        def close(*args):
            self.app.stop()

        self.connect("delete-event", close)

        self._stop_button = Gtk.Button(label="Pause")
        self._stop_button.props.always_show_image = True
        stop_image = Gtk.Image.new_from_icon_name("media-stop", Gtk.IconSize.INVALID)
        self._stop_button.set_image(stop_image)
        self._stop_button.set_action_name("win.stop")

        if self._player.recording:
            record_label = "Stop recording"
        else:
            record_label = "Record"
        self._record_button = Gtk.ToggleButton(label=record_label)
        self._record_button.props.always_show_image = True
        self._record_button.props.active = self._player.recording
        record_image = Gtk.Image.new_from_icon_name("media-record", Gtk.IconSize.INVALID)
        self._record_button.set_image(record_image)
        self._record_button.set_action_name("win.record")

        self._volume_button = Gtk.VolumeButton()
        self._volume_signal_handler = self._volume_button.connect("value-changed",
                                                                  self._volume_changed_cb, None)

        self._mute_button = Gtk.Button()
        self._mute_button.set_action_name("win.mute")

        controls_hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        controls_hbox.pack_start(self._stop_button, True, True, 2)
        controls_hbox.pack_start(self._record_button, True, True, 2)
        controls_hbox.pack_start(self._mute_button, True, True, 2)
        controls_hbox.pack_start(self._volume_button, False, False, 2)

        self._cover = Gtk.Image.new()
        self._artist_label = Gtk.Label()
        self._song_title_label = Gtk.Label()
        self._progress_bar = Gtk.ProgressBar.new()

        stations_combo = Gtk.ComboBoxText()
        stations_combo.set_entry_text_column(0)
        stations_combo.connect("changed", self._radio_changed_cb)
        stations = list(radios.STATIONS.keys())
        stations.sort()
        for name in stations:
            stations_combo.append_text(name)
        stations_combo.set_active(stations.index(self._controller.station_name))

        main_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        main_box.pack_start(stations_combo, False, False, 2)
        main_box.pack_start(self._cover, False, False, 2)
        main_box.pack_start(self._artist_label, True, False, 2)
        main_box.pack_start(self._song_title_label, True, False, 2)
        main_box.pack_start(self._progress_bar, True, True, 2)
        main_box.pack_start(controls_hbox, False, False, 2)

        self.add(main_box)
        self.show_all()

    def _reset_progress_bar(self, controller, delta):
        self._expected_song_duration = delta
        self._next_song_ts = time.time() + delta

    def _update_progress_bar(self):
        if self._next_song_ts == -1:
            return True
        fraction = 1 - ((self._next_song_ts - time.time()) / self._expected_song_duration)
        self._progress_bar.set_fraction(fraction)
        return True

    def _player_suspended(self, player):
        GLib.source_remove(self._progress_bar_update_handler)
        self._progress_bar_update_handler = 0

        image = Gtk.Image.new_from_icon_name("media-playback-start", Gtk.IconSize.INVALID)
        self._stop_button.set_image(image)
        self._stop_button.props.label = "Start"
        self._stop_action.set_state(GLib.Variant.new_boolean(True))

    def _player_resumed(self, player):
        self._progress_bar_update_handler = GLib.timeout_add(200, self._update_progress_bar)
        GLib.source_set_name_by_id(self._progress_bar_update_handler, "cocoricofm-progress-bar")

        image = Gtk.Image.new_from_icon_name("media-playback-stop", Gtk.IconSize.INVALID)
        self._stop_button.set_image(image)
        self._stop_button.props.label = "Stop"
        self._stop_action.set_state(GLib.Variant.new_boolean(False))

    def _player_volume_changed(self, player):
        current_value = self._volume_button.get_value()
        new_value = player.volume
        if abs(current_value - new_value) > 0.01:
            GObject.signal_handler_block(self._volume_button, self._volume_signal_handler)
            self._volume_button.set_value(new_value)
            GObject.signal_handler_unblock(self._volume_button, self._volume_signal_handler)

    def _player_mute_changed(self, player):
        if player.muted:
            self._mute_button.props.label = "Un-mute"
        else:
            self._mute_button.props.label = "Mute"
        self._mute_action.set_state(GLib.Variant.new_boolean(not player.muted))

    def _volume_changed_cb(self, button, value, extra_data):
        GObject.signal_handler_block(self._volume_button, self._volume_signal_handler)
        self._player.set_volume(value)
        GObject.signal_handler_unblock(self._volume_button, self._volume_signal_handler)

    def toggle_mute(self, action, value):
        action.set_state(value)
        self._player.toggle_mute()

    def toggle_stop(self, action, value):
        action.set_state(value)
        self._player.toggle_stop()

    def toggle_recording(self, action, value):
        action.set_state(value)
        self._player.toggle_recording()

    def _player_recording_changed(self, player):
        if self._player.recording:
            record_label = "Stop recording"
        else:
            record_label = "Record"
        self._record_action.set_state(GLib.Variant.new_boolean(self._player.recording))
        self._record_button.props.label = record_label

    async def update(self, song_infos):
        self._artist_label.props.label = song_infos.artist
        self._song_title_label.props.label = song_infos.title

        data = await song_infos.fetch_cover()
        loader = GdkPixbuf.PixbufLoader()
        loader.write(data)
        pixbuf = loader.get_pixbuf()
        if pixbuf:
            self._cover.set_from_pixbuf(pixbuf.scale_simple(self.DEFAULT_WIDTH, 390, GdkPixbuf.InterpType.BILINEAR))
            _, height = self.get_size()
            self.resize(self.DEFAULT_WIDTH, height)

        loader.close()
        del pixbuf
        del loader

    def _radio_changed_cb(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter:
            model = combo.get_model()
            name = model[tree_iter][0]
            if name != self._controller.station_name:
                self._controller.tune_station_with_name(name)


class GUI(Gtk.Application):

    def __init__(self, controller, player, stop_cb):
        super().__init__(application_id="net.base-art.cocoricofm")
        self.window = None
        self.controller = controller
        self.player = player
        self.stop = stop_cb

    async def update(self, song_infos):
        if self.window:
            return await self.window.update(song_infos)

    def do_startup(self):
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

    def on_quit(self, action, param):
        self.stop()
        self.quit()

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self)

        self.window.present()

    def start(self):
        self.register()
        self.activate()

def init():
    Gtk.init([])
    settings = Gtk.Settings.get_default()
    if settings:
        settings.props.gtk_application_prefer_dark_theme = True
