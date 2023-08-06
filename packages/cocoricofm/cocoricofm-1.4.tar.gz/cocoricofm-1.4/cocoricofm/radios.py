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

import urllib.request, urllib.error, urllib.parse
import json
import time
import html.parser
from bs4 import BeautifulSoup
import asyncio
import async_timeout
import os
import pkg_resources
import gbulb
import ssl
import re
from .playlistparser.plparser.common import parse as plparse
from . import httpclient

HTTP_CLIENT = httpclient.HttpClient()

async def fetch(url, raw=False):
    return await HTTP_CLIENT.get(url, raw=raw)

STATIONS={}

class MetaRadio(type):
    def __init__(cls, name, bases, dct):
        super(MetaRadio, cls).__init__(name, bases, dct)
        if name not in ("Radio", "RadioFranceWebRadio", "FIPWebRadio"):
            if 'name' in dct:
                name = dct['name']
            STATIONS[name] = cls

class SongInfos:
    artist = ""
    album = ""
    title = ""
    cover_url = ""
    default_cover_url = ""
    year = 0
    label = ""
    metadata_fetched = False
    duration = 0
    mbid = ""

    def __init__(self, artist, album, title, year, cover_url=''):
        self.artist = artist
        self.album = album
        self.title = title
        self.initial_metadata = (self.artist, self.album, self.title)
        self.cover_url = cover_url
        self.time_started = time.time()

    async def fetch_cover(self):
        future = asyncio.Future()
        if hasattr(self, '_cover_data'):
            future.set_result(self._cover_data)
            return await future
        elif self.cover_url:
            self._cover_data = await fetch(self.cover_url, raw=True)
            return self._cover_data
        elif self.default_cover_url:
            self._cover_data = await fetch(self.default_cover_url, raw=True)
            return self._cover_data
        else:
            self._cover_data = pkg_resources.resource_string('cocoricofm', os.path.join('static', 'no-cover.png'))
            future.set_result(self._cover_data)
            return await future

    def update_metadata(self, artist, album, title, duration, mbid, cover_url=None):
        self.initial_metadata = (self.artist, self.album, self.title)
        self.artist = artist
        self.album = album
        self.title = title
        self.duration = duration
        self.mbid = mbid
        if cover_url:
            self.cover_url = cover_url

    def is_empty(self):
        return self.artist == '' and self.title == ''

    def __eq__(self, other):
        return (self.initial_metadata == other.initial_metadata)

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        return "<SongInfos artist=%r, album=%r, title=%r, cover_url=%r>" % (self.artist, self.album, self.title, self.cover_url)

class Radio(object, metaclass=MetaRadio):
    advising_cache_time = False
    provides_metadata_from_external_source = True
    stream_url = ''

    def next_update_timestamp(self):
        return None

    def server_time(self):
        return time.time()

    async def now_playing(self):
        future = asyncio.Future()
        future.set_result(SongInfos("", "", "", 0))
        return await future

    async def live_url(self):
        future = asyncio.Future()
        if self.stream_url:
            future.set_result(self.stream_url)
            return await future

        data = await fetch(self.playlist_url, raw=True)
        playlist = plparse(filedata=data)
        self.stream_url = playlist.Tracks[0].File
        future.set_result(self.stream_url)
        return await future

    def metadata_tags_to_song_infos(self, tags):
        return SongInfos("", "", "", 0)

class RadioFranceWebRadio(Radio):
    advising_cache_time = True

    def __init__(self):
        super(RadioFranceWebRadio, self).__init__()
        self._cache_expires = None
        self._server_time = None

    def next_update_timestamp(self):
        return self._cache_expires

    def server_time(self):
        if not self._server_time:
            return time.time()
        return self._server_time

    async def now_playing(self):
        graphql = not hasattr(self, 'json_metadata_url')
        if graphql:
            variables = '{"bannerPreset":"600x600-noTransform","stationId":%d,"previousTrackLimit":3}' % self.station_id
            extensions = '{"persistedQuery":{"version":1,"sha256Hash":"8a931c7d177ff69709a79f4c213bd2403f0c11836c560bc22da55628d8100df8"}}'
            tmpl = "https://%s/latest/api/graphql?operationName=Now&variables=%s&extensions=%s"
            url = tmpl % (self.graphql_hostname, urllib.parse.quote(variables),
                          urllib.parse.quote(extensions))
        else:
            now = int(round(time.time()))
            url = "%s?_=%s" % (self.json_metadata_url, now)

        data = await fetch(url)
        try:
            json_data = json.loads(data)
        except:
            return SongInfos('', '', '', 0)

        if graphql:
            item = json_data['data']['now']
            if not item:
                self._server_time = None
                return SongInfos("", "", "", 0)

            song = item['song']

            try:
                title = item['playing_item']['title']
                if title:
                    artist = title.title()
                else:
                    artist = ''
            except KeyError:
                artist = ''

            self._cache_expires = item['next_refresh']
            self._server_time = item['server_time']

            mapping = {'artist': artist, 'year': 0}
            if song:
                for attr in ('album', 'title', 'label'):
                    try:
                        if song[attr]:
                            mapping[attr] = song[attr].title()
                    except KeyError:
                        continue
                try:
                    mapping['cover_url'] = song['cover']
                except KeyError:
                    pass
        else:
            levels = json_data['levels'][len(json_data['levels']) - 1]
            items = levels['items']
            position = levels['position']
            stepId = items[position]
            song = json_data['steps'][stepId]
            self._cache_expires = song['end']

            mapping = {}
            for (attr, key) in (('artist', 'authors'), ('album', 'titreAlbum'),
                                ('title', 'title'), ('label', 'label')):
                try:
                    mapping[attr] = song[key].title()
                except KeyError:
                    continue
            try:
                mapping['cover_url'] = song['visual']
            except KeyError:
                pass

            try:
                mapping['year'] = song['anneeEditionMusique']
            except KeyError:
                pass

        return SongInfos(mapping.get('artist', ''), mapping.get('album', ''),
                         mapping.get('title', ''), mapping.get('year', 0),
                         cover_url=mapping.get('cover_url',''))

class FIPWebRadio(RadioFranceWebRadio):
    graphql_hostname = "www.fip.fr"

    def __init__(self):
        super(FIPWebRadio, self).__init__()
        self.stream_url = "http://direct.fipradio.fr/live/%s" % self.stream_filename

class FIP(FIPWebRadio):
    stream_filename = "fip-midfi.mp3"
    station_id = 7

class FIPRockWebRadio(FIPWebRadio):
    name = "FIP Autour du Rock"
    stream_filename = "fip-webradio1.mp3"
    station_id = 64

class FIPJazzWebRadio(FIPWebRadio):
    name = "FIP Autour du Jazz"
    stream_filename = "fip-webradio2.mp3"
    station_id = 65

class FIPGrooveWebRadio(FIPWebRadio):
    name = "FIP Autour du Groove"
    stream_filename = "fip-webradio3.mp3"
    station_id = 66

class FIPMondeWebRadio(FIPWebRadio):
    name = "FIP Autour du Monde"
    stream_filename = "fip-webradio4.mp3"
    station_id = 69

class FIPNouveauWebRadio(FIPWebRadio):
    name = "FIP Tout Nouveau"
    stream_filename = "fip-webradio5.mp3"
    station_id = 70

class FIPReggaeWebRadio(FIPWebRadio):
    name = "FIP Reggae"
    stream_filename = "fip-webradio6.mp3"
    station_id = 71

class FIPElectroWebRadio(FIPWebRadio):
    name = "FIP Electro"
    stream_filename = "fip-webradio8.mp3"
    station_id = 74

class FIPMetalWebRadio(FIPWebRadio):
    name = "FIP Metal"
    station_id = 77
    stream_filename = "fip-webradio7.mp3"

class FranceInter(Radio):
    stream_url = "http://direct.franceinter.fr/live/franceinter-midfi.mp3"

class FranceMusique(Radio):
    name = "France Musique"
    stream_url = "http://direct.francemusique.fr/live/francemusique-midfi.mp3"

class FranceMusiqueClassiqueEasy(RadioFranceWebRadio):
    name = "France Musique Classique Easy"
    stream_url = "http://direct.francemusique.fr/live/francemusiqueeasyclassique-hifi.mp3"
    json_metadata_url = "https://www.francemusique.fr/livemeta/pull/401"

class FranceMusiqueClassiquePlus(RadioFranceWebRadio):
    name = "France Musique Classique Plus"
    stream_url = "http://direct.francemusique.fr/live/francemusiqueclassiqueplus-hifi.mp3"
    json_metadata_url = "https://www.francemusique.fr/livemeta/pull/402"

class FranceMusiqueConcerts(RadioFranceWebRadio):
    name = "France Musique Concerts"
    stream_url = "http://chai5she.cdn.dvmr.fr/francemusiqueconcertsradiofrance-hifi.mp3"
    json_metadata_url = "https://www.francemusique.fr/livemeta/pull/403"

class FranceMusiqueJazz(RadioFranceWebRadio):
    name = "France Musique Jazz"
    stream_url = "http://chai5she.cdn.dvmr.fr/francemusiquelajazz-hifi.mp3"
    json_metadata_url = "https://www.francemusique.fr/livemeta/pull/405"

class FranceMusiqueContemporaine(RadioFranceWebRadio):
    name = "France Musique Contemporaine"
    stream_url = "http://chai5she.cdn.dvmr.fr/francemusiquelacontemporaine-hifi.mp3"
    json_metadata_url = "https://www.francemusique.fr/livemeta/pull/406"

class FranceMusiqueMonde(RadioFranceWebRadio):
    name = "France Musique du Monde"
    stream_url = "http://chai5she.cdn.dvmr.fr/francemusiqueocoramonde-hifi.mp3"
    json_metadata_url = "https://www.francemusique.fr/livemeta/pull/404"

class FranceMusiqueBO(RadioFranceWebRadio):
    name = "France Musique B.O"
    stream_url = "http://chai5she.cdn.dvmr.fr/francemusiquelevenementielle-hifi.mp3"
    json_metadata_url = "https://www.francemusique.fr/livemeta/pull/407"

class LeMouv(Radio):
    stream_url = "http://direct.mouv.fr/live/mouv-midfi.mp3"

class KCSM(Radio):
    playlist_url = 'http://kcsm.org/KCSM-iTunes-SNS.pls'

    async def now_playing(self):
        url = 'http://kcsm.org/playlist'

        html = await fetch(url, raw=True)
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup('table', {'class': 'listbackground'})[0].findAll('tr')
        artist = rows[0].find('a',{'class':'artist_title'}).text.title()
        title = rows[0].findAll('td')[-1].text.title()
        album = rows[1].find('a').text.title()
        infos = SongInfos(artist, album, title, 0)
        return infos

class TripleJ(Radio):
    playlist_url = 'http://www.abc.net.au/res/streaming/audio/mp3/triplej.pls'

    async def now_playing(self):
        now = int(round(time.time()) / 3e4)
        url =  "http://www.abc.net.au/triplej/feeds/playout/triplej_sydney_playout.xml?_=%s" % now

        html_data = await fetch(url)
        soup = BeautifulSoup(html_data, 'html.parser')
        parser = html.parser.HTMLParser()
        for item in soup('item'):
            if item('playing')[0].text == 'now':
                artist = parser.unescape(item('artistname')[0].text)
                album = parser.unescape(item('albumname')[0].text)
                title = parser.unescape(item('title')[0].text)
                infos = SongInfos(artist, album, title, 0)
                infos.cover_url = parser.unescape(item('albumimage')[0].text)
                return infos
        return SongInfos('', '', '', 0)

class KEXP(Radio):
    stream_url = 'http://live-mp3-128.kexp.org/kexp128.mp3'

    async def now_playing(self):
        url = 'https://legacy-api.kexp.org/play/?limit=5&ordering=-airdate'
        default_cover_url = "http://kexp.org/static/assets/img/default.png"

        data = await fetch(url)
        infos = SongInfos('', '', '', 0)
        infos.default_cover_url = default_cover_url
        try:
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return infos
        item = json_data['results'][0]
        if item['playtype']['playtypeid'] != 4: # 4 is Air break
            artist = item['artist']['name']
            title = item['track']['name']
            release = item['release']
            if release:
                album = release['name']
            else:
                album = ''
            infos = SongInfos(artist, album, title, 0)
            if release and release['largeimageuri']:
                infos.cover_url = release['largeimageuri']
        return infos

class RadioHelsinki(Radio):
    playlist_url = "http://radio.radiohelsinki.fi/rh256"
    name = "Radio Helsinki"

    async def now_playing(self):
        url = "http://www.radiohelsinki.fi/wp-content/djonline.json"

        data = await fetch(url, raw=True)
        try:
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return SongInfos('', '', '', 0)
        playing = json_data['last_playing'][0] or {}
        artist = playing.get('artist', '')
        album = playing.get('album', '')
        song = playing.get('song', '')
        year = playing.get('year', 0)
        infos = SongInfos(artist, album, song, year)
        infos.label = playing.get('label', '')
        return infos

class ByteFM(Radio):
    stream_url = "http://bytefm.cast.addradio.de/bytefm/main/mid/stream"
    name = "ByteFM"

    def __init__(self):
        self._news_regexp = re.compile('[0-9]+ Uhr &ndash; Nachrichten')

    async def now_playing(self):
        url = "https://www.byte.fm/ajax/song-history/"

        data = await fetch(url, raw=True)
        infos = SongInfos('', '', '', 0)
        try:
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return infos
        playing_info = json_data['tracks'][0]
        if (self._news_regexp.match(playing_info)):
            return infos
        playing = playing_info.split(' &ndash; ')
        if (len(playing) < 2):
            return infos
        infos = SongInfos(playing[0], '', playing[1], 0)

        return infos

class DeutschlandfunkNova(Radio):
    stream_url = "http://st03.dlf.de/dlf/03/104/ogg/stream.ogg"
    name = "Deutschlandfunk Nova"
    advising_cache_time = True

    def __init__(self):
        self._cache_expires = None

    def next_update_timestamp(self):
        return self._cache_expires

    async def now_playing(self):
        url = "https://www.deutschlandfunknova.de/actions/dradio/playlist/onair"

        data = await fetch(url, raw=True)
        try:
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return SongInfos('', '', '', 0)
        playing = json_data["playlistItem"]
        if ('stoptime' in playing):
            self._cache_expires = int(playing['stoptime'])
        if not 'artist' in playing or playing['type'] != 'Music' or int(self._cache_expires) < int(round(time.time())):
            infos = SongInfos('', '', '', 0)
            infos.default_cover_url = playing['cover']
            return infos
        infos = SongInfos(playing['artist'], '', playing['title'], 0)
        infos.time_started = int(playing['starttime'])
        # 'cover' is the program's logo, so use it as a default cover.
        if ('cover' in playing):
            infos.default_cover_url = playing['cover']

        return infos

class DeltaRadio(Radio):
    stream_url = "https://delta.hoerradar.de/deltaradio-live-mp3-hq"
    provides_metadata_from_external_source = False

    def metadata_tags_to_song_infos(self, tags):
        info = SongInfos('', '', '', 0)
        if 'title' in tags.keys():
            try:
                artist, title = tags['title'].split(' - ')
            except ValueError:
                pass
            else:
                info = SongInfos(artist, '', title, 0)
        return info

class RockFM(Radio):
    stream_url = 'http://rockfm.cope.stream.flumotion.com/cope/rockfm/playlist.m3u8'

    async def now_playing(self):
        url = 'http://bo.cope.webtv.flumotion.com/api/active?format=json&podId=78'
        data = await fetch(url, raw=True)
        try:
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return SongInfos('', '', '', 0)
        metadata = json.loads(json_data['value'])
        if metadata['title'].lower() == 'rockfm' or not metadata['author']:
            return SongInfos('', '', '', 0)
        # TODO: handle image attr
        return SongInfos(metadata['author'], '', metadata['title'], 0)
