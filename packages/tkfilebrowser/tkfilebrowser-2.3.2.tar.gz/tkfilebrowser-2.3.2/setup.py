#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

from codecs import open
from os import path, name

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()



setup(name='tkfilebrowser',
      version='2.3.2',
      description='File browser for Tkinter, alternative to tkinter.filedialog in linux with GTK bookmarks support.',
      long_description=long_description,
      url='https://github.com/j4321/tkFileBrowser',
      author='Juliette Monsel',
      author_email='j_4321@protonmail.com',
      license='GPLv3',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Widget Sets',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Natural Language :: English',
                   'Natural Language :: French',
                   'Operating System :: POSIX :: Linux',
                   'Operating System :: Microsoft :: Windows'],
      py_modules=["tkfilebrowser.autoscrollbar",
                  "tkfilebrowser.constants",
                  "tkfilebrowser.filebrowser",
                  "tkfilebrowser.functions",
                  "tkfilebrowser.path_button",
                  "tkfilebrowser.recent_files",
                  "tkfilebrowser.tooltip"],
      keywords=['tkinter', 'filedialog', 'filebrowser'],
      packages=["tkfilebrowser"],
      package_data={"tkfilebrowser": ["images/*"]},
      install_requires=["psutil", "babel"] + (['pypiwin32'] if name == 'nt' else []),
      extras_require={'tk<8.6.0': 'Pillow'})
