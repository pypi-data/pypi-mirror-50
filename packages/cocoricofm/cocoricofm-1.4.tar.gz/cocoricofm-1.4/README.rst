
About
=====

A simple radio player implemented in Python3.

.. image:: https://gitlab.com/philn/CocoRicoFM/raw/master/data/screenshot.png


The currently supported radio stations are:

- ByteFM
- Deutschlandfunk Nova
- DeltaRadio
- FIP
- FIP Autour du Groove
- FIP Autour du Jazz
- FIP Autour du Monde
- FIP Autour du Rock
- FIP Electro
- FIP Reggae
- FIP Tout Nouveau
- France Musique
- France Musique B.O
- France Musique Classique Easy
- France Musique Classique Plus
- France Musique Concerts
- France Musique Contemporaine
- France Musique Jazz
- France Musique du Monde
- FranceInter
- KCSM
- LeMouv
- Radio Helsinki
- RockFM
- TripleJ

Dependencies:

- python3
- python3-gbulb
- python-aiohttp
- python-gi
- gstreamer
- gst-plugins-base
- gst-plugins-good
- python-bs4 (BeautifulSoup4)
- python-chardet

Optional dependencies:

- python-lirc
- python-gntp
- pygtk (for the graphical user interface)
- aiohttp_jinja2 and jinja2 for the web remote templates
- pyobjc (for macOS desktop notifications support)


Features:

- notifications of song with libnotify or via python-gntp over the
  network to a Growl daemon
- scrobbling to lastfm (and/or librefm)
- optionally dump the stream to local files
- multimedia keys support (stop, playpause)
- headless mode, when dbus and/or X11 is not available
- limited support for Denon AVR amps, power off/on from remote control
- optional Web remote running on HTTP port 5000.
- optional GTK+ user interface

Dependencies installation
=========================

On Linux
--------

::

    # apt install gstreamer1.0-plugins-{base,good,bad} libsoup2.4-1 python3-pip gir1.2-gst-plugins-base-1.0 gir1.2-gtk-3.0
    # apt install liblirc-dev
    $ pip3 install --user .
    $ pip3 install --user requirements_linux.txt
    $ xdg-user-dirs-update

On macOS
--------

Some of the dependencies can be installed with Homebrew:

::

    $ brew install python3 gobject-introspection libsoup gtk+3 gstreamer gst-plugins-{base,good,bad} gst-python

And the remaining Python packages using pip, optionally inside a dedicated virtualenv:

::

    $ pip3 install -r .
    $ pip3 install -r requirements_macOS.txt


Running the app
===============

To run without installing, from the project root directory:

::

    $ python3 -m cocoricofm [options]

To install:

- Use gen_pylast_md5sum.py to get your password hashes for libre.fm/last.fm
- Copy cocoricofm.cfg.sample to ~/.config/cocoricofm.cfg and edit accordingly
- Run either one of these commands:

  ::

    $ sudo python3 setup.py develop
    $ sudo python3 setup.py install

- A cocoricofm executable script should now be available in your $PATH.
