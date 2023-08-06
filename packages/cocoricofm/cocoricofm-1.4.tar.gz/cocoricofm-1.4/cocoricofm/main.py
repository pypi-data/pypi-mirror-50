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

import optparse
import os, sys
import configparser

from gi.repository import GLib, GObject
from . import version

def main(args=None, usage=None):
    if not args:
        args = sys.argv[1:]

    default_music_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_MUSIC)
    default_station = "FIP"
    parser = optparse.OptionParser(usage=usage, version="CocoRicoFM %s" % version)
    parser.add_option("-i", "--interval", dest="interval", default=60, type=int,
                      help="scraping interval in seconds")
    parser.add_option("-r", "--record",
                      dest="record", action="store_true", default=False,
                      help="Record each song played to a specific file in given directory")
    parser.add_option("-o", "--output",
                      dest="output", default=default_music_dir,
                      help="Directory where to store recorded songs")
    parser.add_option("-s", "--station",
                      dest="station", help="Radio to tune to. Default: %s" % default_station)
    parser.add_option("-n", "--no-scrobble", action="store_true", default=False,
                      dest="noscrobble",
                      help="disable scrobbling")
    parser.add_option("-l", "--list-stations", action="store_true", default=False,
                      dest="list_stations",
                      help="display the list of radio stations")
    parser.add_option("-x", "--headless", action="store_true", default=False,
                      dest="headless",
                      help="disable desktop notifications")
    parser.add_option("-g", "--gui", action="store_true", default=False,
                      dest="gui",
                      help="enable GTK+ user interface")
    parser.add_option("-p", "--port", dest="port", default=0, type=int,
                      help="HTTP port to listen to for the Web remote. Default: 0. The Web remote is disabled by default, to enable set the port to a positive number")
    parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true",
                      help="Logs debug messages to stdout")
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                      help="Logs verbose debug messages to stdout")

    (options, args) = parser.parse_args(args)

    if options.list_stations:
        from .radios import STATIONS
        print("Supported radio stations:")
        stations = list(STATIONS.keys())
        stations.sort()
        for name in stations:
            print("- %s" % name)
        return 0

    if args:
        cfgfile = args[0]
    else:
        cfgfile = os.path.expanduser("~/.config/cocoricofm.cfg")

    config = configparser.ConfigParser()
    if os.path.exists(cfgfile):
        config.read(cfgfile)

    GObject.threads_init()
    GLib.set_prgname("CocoricoFM")
    GLib.setenv("PA_PROP_MEDIA_ROLE", "music", True)
    GLib.setenv("PA_PROP_MEDIA_ICON_NAME", "audio-x-mp3", True)

    from .controller import Controller, InitializationError
    try:
        controller = Controller(options, config, default_station)
    except InitializationError:
        logging.error("Controller failed to initialize")
        return 1
    else:
        return controller.run()
