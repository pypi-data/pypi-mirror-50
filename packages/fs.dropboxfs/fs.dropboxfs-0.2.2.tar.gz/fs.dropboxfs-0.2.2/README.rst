fs.dropboxfs
============

``fs.dropboxfs`` is a Dropbox driver for PyFileSystem2.


Supported Python versions
-------------------------

- Python 2.7
- Python 3.5
- Python 3.6
- Python 3.7
- PyPy

Usage
-----

Use the ``fs.open_fs`` method with the ``dropbox://`` protocol:

.. code:: python

    >>> import fs
    >>> handle = fs.open_fs('dropbox://dropbox.com?access_token=<dropbox access token>')

Repository
----------

- https://github.com/PyFilesystem/fs.dropboxfs

Issue tracker
-------------

- https://github.com/PyFilesystem/fs.dropboxfs/issues

Tests
-----

- https://travis-ci.org/PyFilesystem/fs.dropboxfs/builds

Author and contributors
-----------------------

- Rehan Khwaja
- Andreas Jung


License
-------

This module is published under the MIT license.

This module was partly and financed by Andreas Jung/ZOPYX


Contact
-------

| Andreas Jung/ZOPYX
| Hundskapfklinge 33
| D-72074 Tübingen
| info@zopyx.com
| www.zopyx.com

