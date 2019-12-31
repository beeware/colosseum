.. _tutorial-1:

===========================
Your first Colosseum layout
===========================

In a virtualenv, install Colosseum::

    $ pip install colosseum

Colosseum provides a ``CSS`` class that allows you to define CSS properties and
apply them to any DOM-like tree of objects. There is no required base class;
Colosseum will duck-type any object providing the required API. The simplest
possible DOM node is the following::

    from colosseum.dimensions import Size, Box

    class MyDOMNode:
        def __init__(self, style):
            self.parent = None
            self.children = []
            self.intrinsic = Size(self)
            self.layout = Box(self)
            self.style = style.copy(self)

        def add(self, child):
            self.children.append(child)
            child.parent = self


That is, a node must provide:

* a ``parent`` attribute, declaring the parent in the DOM tree; the root
  of the DOM tree has a ``parent`` of ``None``.

* a ``children`` attribute, containing the list of DOM child nodes.

* an ``intrinsic`` attribute, storing any intrinsic size hints for the node.

* a ``layout`` attribute, for storing the final position of the node.

* a ``style`` attribute - generally a ``CSS`` declaration, bound to the node.

We also need an area on to which we're going to render. This could be a screen,
a page, a canvas, or any other rectangular content area. Again, colosseum will
duck-type any class that has the required API::

    class Page:
        def __init__(self, width, height):
            self.content_width = width
            self.content_height = height


With a compliant DOM node definition, you can create a content page, an
instance of the DOM node class, and some children for that node::

    >>> from colosseum import CSS
    >>> from colosseum.constants import BLOCK
    >>> page = Page(2000, 2000)
    >>> node = MyDOMNode(style=CSS(display=BLOCK, width=1000, height=1000))
    >>> node.add(MyDOMNode(style=CSS(display=BLOCK, width=100, height=200)))
    >>> node.add(MyDOMNode(style=CSS(display=BLOCK, width=300, height=150)))

You can then ask for a layout to be computed, and query the results::

    >>> from colosseum.engine import layout
    >>> layout(page, node)
    >>> print(node.layout)
    <Box (1000x2000 @ 0,0)>
    >>> node.layout.content_width
    1000
    >>> node.layout.content_width
    2000
    >>> node.layout.content_top
    0
    >>> node.layout.content_left
    0
    >>> for child in node.children:
    ...     print(child.layout)
    <Box (100x200 @ 0,0)>
    <Box (300x150 @ 0,200)>

Note that although the root node specifies a height of 1000, the computed
content size is 2000 (i.e., the size of the display area). This matches how
the root element is sized in a HTML5 document.

Style attributes can also be set in bulk, using the ``update()`` method on
the style attribute::

    >>> node.style.update(width=1500, height=800)
    >>> layout(page, node)
    >>> print(node.layout)
    <Box (1500x2000 @ 0,0)>

Style attributes can also be removed by deleting the attribute on the
style attribute. The value of the property will revert to the default::

    >>> node.style.update(margin_top=10, margin_left=20)
    >>> layout(page, node)
    >>> print(node.layout)
    <Box (1500x800 @ 20,10)>
    >>> del(node.style.margin_left)
    >>> layout(display, node)
    >>> print(node.style.margin_left)
    0
    >>> print(node.layout)
    <Box (1500x800 @ 0,10)>
