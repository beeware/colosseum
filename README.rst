.. image:: http://pybee.org/static/images/defaultlogo.png
    :width: 72px
    :target: https://pybee.org/colosseum

Colosseum
=========

.. image:: https://img.shields.io/pypi/pyversions/colosseum.svg
    :target: https://pypi.python.org/pypi/colosseum

.. image:: https://img.shields.io/pypi/v/colosseum.svg
    :target: https://pypi.python.org/pypi/colosseum

.. image:: https://img.shields.io/pypi/status/colosseum.svg
    :target: https://pypi.python.org/pypi/colosseum

.. image:: https://img.shields.io/pypi/l/colosseum.svg
    :target: https://github.com/pybee/colosseum/blob/master/LICENSE

.. image:: https://travis-ci.org/pybee/colosseum.svg?branch=master
    :target: https://travis-ci.org/pybee/colosseum

.. image:: https://badges.gitter.im/pybee/general.svg
    :target: https://gitter.im/pybee/general

An independent implementation of the CSS layout algorithm. This
implementation is completely standalone - it isn't dependent on
a browser, and can be run over any box-like set of objects that
need to be laid out on a page (either physical or virtual)

At present, the implementation is partial; only **portions** of
the box and flexbox section of the specification are defined:

==========================================================================================  =======================================================================================
Name                                                                                        Value
==========================================================================================  =======================================================================================
width, height                                                                               positive number
min_width, min_height                                                                       positive number
max_width, max_height                                                                       positive number
left, right, top, bottom                                                                    number
margin, margin_left, margin_right, margin_top, margin_bottom                                number
padding, padding_left, padding_right, padding_top, padding_bottom                           positive number
border_width, border_left_width, border_right_width, border_top_width, border_bottom_width  positive number
flex_direction                                                                              ``"column"``, ``"row"``
justify_content                                                                             ``"flex-start"``, ``"center"``, ``"flex-end"``, ``"space-between"``, ``"space-around"``
align_items, align_self                                                                     ``"flex-start"``, ``"center"``, ``"flex-end"``, ``"stretch"``
flex                                                                                        positive number
flex_wrap                                                                                   ``"wrap"``, ``"nowrap"``
position                                                                                    ``"relative"``, ``"absolute"``
==========================================================================================  =======================================================================================

Quickstart
----------

In your virtualenv, install Colosseum::

    $ pip install colosseum

Colosseum provides a ``CSS`` class that allows you to define CSS
properties, and apply them can be applied to any DOM-like tree of
objects. There is no required base class; Colosseum will duck-type
any object providing the required API. The simplest possible DOM
node is the following::

    from colosseum import Layout

    class MyDOMNode:
        def __init__(self, style):
            self.parent = None
            self.children = []
            self.layout = Layout(self)
            self.style = style.bind(self)

        def add(self, child):
            self.children.append(child)
            child.parent = self


That is, a node must provide:

* a ``parent`` attribute, declaring the parent in the DOM tree; the root
  of the DOM tree has a ``parent`` of ``None``.

* a ``children`` attribute, containing the list of DOM child nodes.

* a ``layout`` attribute, for storing the final position of the node.

* a ``style`` attribute - generally a ``CSS`` declaration, bound to the node.

With that a compliant DOM node definition, you can then and query the layout
that results::

    >>> from colosseum import CSS, ROW, COLUMN
    >>> node = MyDOMNode(style=CSS(width=1000, height=1000, flex_direction=ROW))
    >>> node.add(MyDOMNode(style=CSS(width=100, height=200)))
    >>> node.add(MyDOMNode(style=CSS(width=300, height=150)))
    >>> node.style.apply()
    >>> layout = node.layout
    >>> print(node.layout)
    <Layout (1000x1000 @ 0,0)>
    >>> layout.width
    1000
    >>> layout.height
    1000
    >>> layout.top
    0
    >>> layout.left
    0
    >>> for child in node.children:
    ...     print(child.layout)
    <Layout (100x200 @ 0,0)>
    <Layout (300x150 @ 100,0)>

Calling ``node.style.apply()`` forces the box model to be evaluated. Once
evaluated, the layout will be cached. Modifying any CSS property on a node
will mark the layout as dirty, and calling ``apply()`` again will cause the
layout to be re-evaluated. For example, if we switch the outer node to be a
"column" flex box, rather than a "row" flex box, you'll see the coordinates of
the child boxes update to reflect a vertical, rather than horizontal layout::

    >>> node.style.flex_direction = COLUMN
    >>> node.style.apply()
    >>> print(node.layout)
    <Layout (1000x1000 @ 0,0)>
    >>> for child in node.children:
    ...     print(child.layout)
    <Layout (100x200 @ 0,0)>
    <Layout (300x150 @ 0,200)>

If the layout is *not* dirty, the layout will *not* be recomputed.

Style attributes can also be set in bulk, using the ``set()`` method on
the style attribute::

    >>> node.style.set(width=1500, height=800)
    >>> node.style.apply()
    >>> print(node.layout)
    <Layout (1500x800 @ 0,0)>

Style attributes can also be removed by deleting the attribute on the
style attribute. The value of the property will revert to the default::

    >>> node.style.set(margin_top=10, margin_left=20)
    >>> node.style.apply()
    >>> print(node.layout)
    <Layout (1500x800 @ 20,10)>
    >>> del(node.style.margin_left)
    >>> print(node.style.margin_left)
    0
    >>> print(node.layout)
    <Layout (1500x800 @ 0,10)>

Layout values are given relative to their parent node. If you want to
know the absolute position of a node on the display canvas, you can
request the `origin` attribute of the layout. This will give you the
point on the canvas from which all the node's attributes are measured.
You can also request the `absolute` attribute of the layout, which will
give you the position of the element on the entire canvas::

    >>> node.style.set(margin_top=10, margin_left=20)
    >>> node.style.apply()
    >>> print(node.layout)
    <Layout (1500x800 @ 20,10)>
    >>> for child in node.children:
    ...     print(child.layout)
    <Layout (100x200 @ 0,0)>
    <Layout (300x150 @ 0,200)>
    >>> print(node.style.layout.origin)
    <Point (0,0)>
    >>> for child in node.children:
    ...     print(child.style.layout.origin)
    <Point (20,10)>
    <Point (20,10)>
    >>> print(node.style.layout.absolute)
    <Point (20,10)>
    >>> for child in node.children:
    ...     print(child.style.layout.absolute)
    <Point (20,10)>
    <Point (20,210)>


Community
---------

Colosseum is part of the `BeeWare suite`_. You can talk to the community through:

* `@pybeeware on Twitter`_

* The `pybee/general`_ channel on Gitter.

We foster a welcoming and respectful community as described in our
`BeeWare Community Code of Conduct`_.

Contributing
------------

If you experience problems with Colosseum, `log them on GitHub`_. If you
want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _BeeWare suite: http://pybee.org
.. _Read The Docs: https://colosseum.readthedocs.io
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _pybee/general: https://gitter.im/pybee/general
.. _BeeWare Community Code of Conduct: http://pybee.org/community/behavior/
.. _log them on Github: https://github.com/pybee/colosseum/issues
.. _fork the code: https://github.com/pybee/colosseum
.. _submit a pull request: https://github.com/pybee/colosseum/pulls

Acknowledgements
----------------

The algorithm and test suite for this library is a language port of
`CSS-layout`_ project, open-sourced by Facebook.

.. _CSS-layout: https://github.com/facebook/css-layout
