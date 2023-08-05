.. image:: https://img.shields.io/badge/dynamic/json.svg?url=https://api.bitbucket.org/2.0/repositories/557058:818b45a5-8b1c-4614-a8e8-e938f448b93c/chronologer/pipelines/?page=1%26pagelen=1%26sort=-created_on%26target.ref_name=frontend&label=build&query=$.values[0].state.result.name&colorB=blue
   :target: https://bitbucket.org/saaj/chronologer/addon/pipelines/home#!/results/branch/frontend/page/1
.. image:: https://badge.fury.io/py/ChronologerUI.svg
   :target: https://pypi.org/project/ChronologerUI/

==============
Chronologer UI
==============

.. figure:: https://bitbucket.org/saaj/chronologer/raw/53816c9dfba77791492438c0f7eb14fc96fae998/source/resource/clui/image/logo/logo240.png
   :alt: Chronologer

Chronologer UI is a browser user interface for `Chronologer`_, a simple Python logging HTTP server.

Chronologer UI is a single-page `Qooxdoo`_ 5 application written in ECMAScript 5.1.


.. _chronologer: https://bitbucket.org/saaj/chronologer/src/backend/
.. _qooxdoo: http://www.qooxdoo.org/


Building frontend
=================
To install dependencies::

  ./generate.py load-library

To make a development build and serve it locally::

  ./generate.py && ./generate.py source-server

To run the test suite in terminal::

  ./generate.py test-console && ./generate.py testsuite

To make the Python distribution package::

  python3 setup.py sdist

Feature list
============
* Tabbed table UI with clone-able tabs
* Ace-based YAML viewer for JSON log records
* D3.js logging timeline
* Log record neighbourhood selection on the timeline
* Extended ISO 8601 format, date ± duration, for absolute and/or relative data and time bounds
* Lucene-like query representation format
* JSON tree leaf projection to table columns

Browser support
===============
Firefox and Chromium of latest stable versions.

Credits
=======
Logo is contributed by `lightypaints`_.


.. _lightypaints: https://www.behance.net/lightypaints

