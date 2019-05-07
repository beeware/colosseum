Release History
===============

0.2.0
-----

From scratch rewrite, using Travertino base classes.

v0.1.6
------

* Fixed the MANIFEST.in file.

v0.1.5
------

* Modify hints so that they only mark layout as modified if the value changes.

v0.1.4
------

* Made the dirty flag a tri-state variable, to allow for "layout in progress" tracking.

v0.1.3
------

* Added ability to extract absolute position of DOM nodes

v0.1.2
------

* Added first W3C-based test suite.
* Added hinting for style objects.
* Separated style definition from DOM definition.

v0.1.1
------

* Added protection against invalid values for string-based properties.
* Added support for bulk setting of attributes.

v0.1.0
------

Initial release of a version based on a port of Facebook's CSS-layout (now `Yoga <https://github.com/facebook/yoga>`__) project.
