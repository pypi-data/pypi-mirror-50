# -*- coding: utf-8 -*-
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

import configparser
import time
from gi.repository import GLib, GObject
import asyncio
import gbulb
import os
import logging

from . import player, radios, pylast, lirc_input, denon, keyboard_input

try:
    from . import linux_notify
except ImportError:
    linux_notify = None

try:
    from . import growl_notify
except ImportError:
    growl_notify = None

try:
    from . import osx_notify
except ImportError:
    osx_notify = None

try:
    from . import web_remote
except ImportError:
    web_remote = None

try:
    from . import ui
except:
    ui = None

class InitializationError(Exception):
    pass

class Controller(GObject.GObject):
    __gsignals__ = { 'station-changed': (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ()),
                     'next-refresh-in': (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (GObject.TYPE_FLOAT,)),
    }

    def __init__(self, options, config, default_station):
        super(Controller, self).__init__()
        gbulb.install(gtk = ui and options.gui)
        self.loop = gbulb.get_event_loop()

        extra_logging_kws = {}
        if options.debug:
            extra_logging_kws['level'] = logging.DEBUG
        if options.verbose:
            extra_logging_kws['level'] = logging.INFO
        logging.basicConfig(format='%(asctime)s [%(levelname)-8s] %(message)s', **extra_logging_kws)

        self.interval = options.interval
        self.recording = options.record
        self.output_path = options.output
        self.disable_scrobble = options.noscrobble
        self.headless = options.headless
        self.ui_enabled = options.gui
        self.http_port = options.port
        self.config = config
        self.lastfm = None
        self.current_song_infos = radios.SongInfos('', '', '', 0)

        growl_credentials = [dict(self.config.items(s)) for s in self.config.sections() if s.startswith("growl")]
        if growl_credentials and not growl_notify:
            logging.warning("Growl notifications disabled. gntp missing?")
        if self.http_port > 0 and not web_remote:
            logging.warning("web_remote disabled. Jinja2 and/or aiohttp_jinja2 missing?")
        if self.ui_enabled and not ui:
            logging.error("PyGTK missing?")
            raise InitializationError

        self.player = player.Player(self)
        self.player.connect("suspended", self._player_suspended)
        self.player.connect("resumed", self._player_resumed)
        self.player.connect("tags-updated", self._player_tags_updated)
        self.player.connect("recording-changed", self._player_recording_changed)

        self._cache_directory = os.path.join(GLib.get_user_cache_dir(), "cocoricofm")
        self._last_station_absolute_path = os.path.join(self._cache_directory, "last-station.txt")

        if (options.station):
            self.station_name = options.station
        else:
            try:
                with open(self._last_station_absolute_path) as f:
                    name = f.readline().strip()
                    if name not in radios.STATIONS.keys():
                        logging.warning("Invalid station name: %r. Falling back to %s" % (name, default_station))
                        station_name = default_station
                    else:
                        station_name = name
            except FileNotFoundError:
                station_name = default_radio

            self.station_name = station_name

        self.suspended = False

        self.previous_status = None
        if not self.headless:
            if osx_notify:
                self.notification = osx_notify.Notification("CocoRicoFM")
            elif linux_notify:
                self.notification = linux_notify.Notification("CocoRicoFM")
            else:
                self.notification = None
        elif growl_notify:
            try:
                self.notification = growl_notify.Notification("CocoRicoFM", growl_credentials)
            except Exception as exc:
                self.notification = None
        else:
            self.notification = None

        self.connect("station-changed", self._station_changed)

        self.ui = None
        if ui and self.ui_enabled:
            ui.init()
            self.ui = ui.GUI(self, self.player, self.main_quit)

        self.keyboard_input = keyboard_input.KeyboardInput(self)
        self.lirc_input = lirc_input.LircInput(config, self)

        try:
            denon_address = self.config.get("denon", "address")
        except configparser.NoSectionError:
            self.denon_remote = None
        else:
            self.denon_remote = denon.DenonRemote(denon_address)

        if web_remote and self.http_port > 0:
            self.web_remote = web_remote.WebRemote(self)
        else:
            self.web_remote = None

    def _station_changed(self, *args):
        asyncio.ensure_future(self.refresh())

    def _sorted_stations(self):
        if hasattr(self, '_stations'):
            return self._stations
        stations = list(radios.STATIONS.keys())
        stations.sort()
        self._stations = stations
        return self._stations

    def current_station_index(self):
        return self._sorted_stations().index(self.station_name)

    def tune(self, station_index):
        stations = self._sorted_stations()
        if station_index in range(len(stations)):
            self.tune_station_with_name(stations[station_index])

    def tune_station_with_name(self, name):
        self.previous_status = None
        self.station_name = name
        self.emit("station-changed")

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)

        if attr == 'station_name':
            self.station = radios.STATIONS[self.station_name]()

            async def tune_url():
                live_url = await self.station.live_url()
                self.player.set_url(live_url)

            asyncio.ensure_future(tune_url())

    def _player_suspended(self, player):
        self.suspended = True
        if not self.previous_status:
            return
        if not self.notification:
            return
        self.notification.clear_actions()
        self.notification.add_action("resume", "Resume playback", self._resume_playback_cb)
        self.notification.icon_name = "media-playback-stop-symbolic"
        asyncio.ensure_future(self.notification.show())

    def _player_resumed(self, player):
        self.suspended = False
        if not self.previous_status:
            return
        if not self.notification:
            return
        self.notification.clear_actions()
        self.notification.add_action("suspend", "Suspend playback", self._suspend_playback_cb)
        self.notification.icon_name = "media-playback-start-symbolic"
        asyncio.ensure_future(self.notification.show())

    def _resume_playback_cb(self, notification, action):
        self.player.start()

    def _suspend_playback_cb(self, notification, action):
        self.player.stop()

    def _player_tags_updated(self, player):
        tags = player.metadata_tags
        infos = self.station.metadata_tags_to_song_infos(tags)
        if not infos.is_empty():
            asyncio.ensure_future(self.process_song_infos(infos))

    def _player_recording_changed(self, player):
        self.recording = player.recording

    async def login(self):
        if self.disable_scrobble:
            return
        if not self.interval:
            return

        self.lastfm = self.librefm = None

        try:
            lastfm_username = self.config.get("scrobbler-lastfm", "user")
            lastfm_pw_hash = self.config.get("scrobbler-lastfm", "password_hash")
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            lastfm_username = None
            lastfm_pw_hash = None
        if lastfm_username and lastfm_pw_hash:
            self.lastfm = pylast.LastFMNetwork(api_key="623bbd684658a8eaaa4066037d3c1531",
                                               api_secret="547e71d1582dfb73f6857444992fa629",
                                               username=lastfm_username,
                                               password_hash=lastfm_pw_hash)
            await self.lastfm.authenticate()
            # TODO: local scrobble cache support
        try:
            librefm_username = self.config.get("scrobbler-librefm", "user")
            librefm_pw_hash = self.config.get("scrobbler-librefm", "password_hash")
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            librefm_username = None
            librefm_pw_hash = None
        if librefm_username and librefm_pw_hash:
            logging.info("LibreFM support is temporarily disabled.")
            #self.librefm = pylast.get_librefm_network(username=librefm_username,
            #                                          password_hash=librefm_pw_hash)

    async def complete_metadata(self, song_infos):
        if not song_infos:
            return None

        if not self.lastfm:
            song_infos.metadata_fetched = True

        artist_name = song_infos.artist
        track_name = song_infos.title
        if not artist_name or not track_name:
            song_infos.metadata_fetched = True

        if song_infos.metadata_fetched:
            return song_infos

        search_results = self.lastfm.search_for_track(artist_name, track_name)
        page = await self._execute_with_pylast(getattr(search_results, "get_next_page"))
        if not page or not len(page):
            return song_infos

        optional_metadata = {}
        album_title = song_infos.album
        cover_url = song_infos.cover_url

        track = page[0]
        album = await self._execute_with_pylast(track.get_album)
        if album:
            if not album_title:
                album_title = album.title
            if (self.ui_enabled or self.recording) and not cover_url:
                cover_url = await self._execute_with_pylast(album.get_cover_image,
                                                            __default=song_infos.default_cover_url)
                optional_metadata['cover_url'] = cover_url
        duration = await self._execute_with_pylast(track.get_duration, __default=0)
        if duration:
            duration = int(duration / 1000.)
        mbid = await self._execute_with_pylast(track.get_mbid, __default="")

        song_infos.update_metadata(track.artist.name, album_title, track.title, duration, mbid, **optional_metadata)
        song_infos.metadata_fetched = True
        return song_infos

    async def _execute_with_pylast(self, function, *args, **kwargs):
        if '__default' in kwargs.keys():
            default_result = kwargs['__default']
            del kwargs['__default']
        else:
            default_result = None

        try:
            result = await function(*args, **kwargs)
        except Exception as exc:
            # Something went wrong, try 2 more times and die.
            attempts = 2
            while attempts > 0:
                try:
                    result = await function(*args, **kwargs)
                except Exception as exc:
                    attempts -= 1
                    continue
                else:
                    break
            if not attempts:
                logging.warning("Call to %r failed..." % function)
                result = default_result

        return result

    async def scrobble_update_now_playing(self, song_infos):
        if self.disable_scrobble:
            return
        if not song_infos:
            return

        if not song_infos.metadata_fetched:
            song_infos = await self.complete_metadata(song_infos)

        if self.lastfm:
            await self._execute_with_pylast(getattr(self.lastfm, "update_now_playing"), song_infos.artist, song_infos.title,
                                            album=song_infos.album, duration=song_infos.duration, mbid=song_infos.mbid)

    async def scrobble_song(self, song_infos):
        if self.disable_scrobble:
            return
        if not song_infos:
            return

        if not song_infos.metadata_fetched:
            await self.complete_metadata(song_infos)

        artist = song_infos.artist
        title = song_infos.title
        if '' not in (artist, title):
            args = (artist, title, song_infos.time_started)
            kwargs = dict(album=song_infos.album)
            if song_infos.mbid:
                kwargs['mbid'] = song_infos.mbid
            if song_infos.duration:
                kwargs['duration'] = song_infos.duration
            for network in (self.lastfm, self.librefm):
                if not network:
                    continue
                await self._execute_with_pylast(getattr(network, "scrobble"), *args, **kwargs)

    def stop(self, emit_signal=True):
        if self.player:
            self.player.stop(emit_signal=emit_signal)
        self.loop.stop()

    def status(self, song_infos):
        artist = song_infos.artist
        album = song_infos.album
        title = song_infos.title
        status = "♫ %s ‒ %s ♫" % (artist, title)
        if self.notification:
            self.notification.update(self.station_name, status)
            if not self.notification.actions:
                self.notification.add_action("suspend", "Suspend playback", self._suspend_playback_cb)
            self.notification.icon_name = "media-playback-start-symbolic"
            asyncio.ensure_future(self.notification.show())

        GLib.setenv("PA_PROP_MEDIA_ARTIST", artist, True)
        GLib.setenv("PA_PROP_MEDIA_TITLE", title, True)
        return "%s: %s" % (self.station_name, status)

    def has_new_track_started(self, track):
        return "" not in (track.artist, track.title) and (not self.previous_status or (track != self.previous_status))

    def has_previous_track_ended(self, track):
        if not self.previous_status:
            return True
        return (self.previous_status != track)

    async def process_song_infos(self, infos):
        if infos.is_empty():
            if self.ui:
                asyncio.ensure_future(self.ui.update(infos))
            return

        self.current_song_infos = infos
        if self.has_previous_track_ended(infos):
            self.player.song_changed(self.previous_status)
            infos = await self.complete_metadata(infos)
            if self.ui:
                asyncio.ensure_future(self.ui.update(infos))
            message = self.status(infos)
            print(message)
            await self.scrobble_song(self.previous_status)

        if self.has_new_track_started(infos):
            await self.scrobble_update_now_playing(infos)
            self.keyboard_input.grab_keys()

        self.previous_status = infos

    async def refresh(self):
        if not self.station.provides_metadata_from_external_source:
            return self.interval

        delta = 0.0
        current = await self.station.now_playing()
        if self.has_new_track_started(current):
            if self.station.advising_cache_time:
                next_update_ts = self.station.next_update_timestamp()
                if next_update_ts:
                    delta = next_update_ts - self.station.server_time()
                    if delta <= 0:
                        delta = 1.0
                else:
                    delta = 1.0

        elif self.station.advising_cache_time:
            delta = 1.0

        if not delta:
            delta = self.interval

        await self.process_song_infos(current)

        return delta

    async def main(self):
        try:
            await self.login()
        except Exception as exc:
            logging.error("Login to scrobble service failed: %s" % exc)
            self.disable_scrobble = True

        while True:
            if self.suspended:
                while self.suspended:
                    await asyncio.sleep(1)

            delta = await self.refresh()
            self.emit('next-refresh-in', delta)
            try:
                await asyncio.sleep(delta)
            except asyncio.CancelledError:
                self.previous_status = None
                if self.notification:
                    await self.notification.close()
                break

        self.stop(emit_signal=False)

    def main_quit(self):
        self.main_task.cancel()

    def run(self):
        self.main_task = asyncio.ensure_future(self.main())

        if self.web_remote:
            asyncio.ensure_future(self.web_remote.start())

        if self.ui:
            self.ui.start()

        asyncio.ensure_future(self.lirc_input.start())

        try:
            self.loop.run_until_complete(self.main_task)
        except KeyboardInterrupt:
            self.main_quit()
            try:
                self.loop.run_until_complete(self.main_task)
            except KeyboardInterrupt:
                pass
            self.main_task.exception()
        finally:
            self.loop.close()
            if not os.path.isdir(self._cache_directory):
                os.makedirs(self._cache_directory)
            with open(self._last_station_absolute_path, "w") as f:
                f.write(self.station_name)

        return 0
