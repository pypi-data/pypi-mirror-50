
catt-qt
=======

Cast All The Things Qt GUI

Written using catt api and pychromecast

Features:


* Able to cast files, links and playlist urls
* Control muliple chromecasts selectable from list
* Get data in real time and shows changes from other devices
* Supports device reboot with initial volume setting
* Manage streams started by other devices
* Play/Pause/Stop/Seek/Volume/Reboot
* Multi-platform

Limitations:


* Takes about 8 seconds to scan for chromecasts when started
* Requires pychromecast 3.2.3 or `this patch <https://github.com/balloob/pychromecast/commit/15655117236b4d856677d5c58a0a29883665003a>`_ for detecting reboots properly
* Services that require login or complicated clicks in browser to play need to be started from a browser or other device

Install:


* ``pip3 install cattqt`` will install from `pypi <https://pypi.org/project/cattqt/>`_

Run:


* ``catt-qt``


.. image:: https://github.com/soreau/catt-qt/blob/master/screenshots/x11.png
   :target: https://github.com/soreau/catt-qt/blob/master/screenshots/x11.png
   :alt: X11


.. image:: https://github.com/soreau/catt-qt/blob/master/screenshots/wayland.png
   :target: https://github.com/soreau/catt-qt/blob/master/screenshots/wayland.png
   :alt: Wayland


.. image:: https://github.com/soreau/catt-qt/blob/master/screenshots/osx.png
   :target: https://github.com/soreau/catt-qt/blob/master/screenshots/osx.png
   :alt: OSX


.. image:: https://github.com/soreau/catt-qt/blob/master/screenshots/windows.png
   :target: https://github.com/soreau/catt-qt/blob/master/screenshots/windows.png
   :alt: Windows

