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

from setuptools import setup, find_packages
from cocoricofm import version
import os

data_files = [os.path.join("data", f) for f in os.listdir("data")]
data_files.extend(["requirements_linux.txt", "requirements_macOS.txt", "README.rst"])

readme = open('README.rst').read()

setup(name="cocoricofm",
      version=version,
      description="A little radio player",
      long_description=readme,
      author="Philippe Normand",
      author_email='phil@base-art.net',
      license="GPL3",
      packages=find_packages(),
      package_data={
          'cocoricofm': ['templates/*.html', 'static/*.js', 'static/*.png'],
      },
      data_files=data_files,
      url="https://gitlab.com/philn/CocoRicoFM/",
      keywords=['radio', 'multimedia', 'gstreamer', 'recording', 'gtk+',
                'libre.fm', 'last.fm'],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Environment :: MacOS X', 'Environment :: Web Environment',
                   'Environment :: X11 Applications :: GTK',
                   'Framework :: AsyncIO',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: Multimedia :: Sound/Audio :: Players',
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   ],
      entry_points="""\
      [console_scripts]
      cocoricofm = cocoricofm.main:main
      """,
      install_requires=[
          "async-timeout==3.0.0",
          "beautifulsoup4==4.6.1",
          "bs4==0.0.1",
          "chardet==3.0.4",
          "gbulb==0.6.1",
          "Jinja2==2.10",
          "MarkupSafe==1.0",
          "six==1.11.0",
      ]
)
