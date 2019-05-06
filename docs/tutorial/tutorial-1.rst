.. _tutorial-1:

===========================
Your first Colosseum layout
===========================

In a virtualenv, install Colosseum::

    $ pip install colosseum

Colosseum provides a ``CSS`` class that allows you to define CSS
properties, and apply them can be applied to any DOM-like tree of
objects. There is no required base class; Colosseum will duck-type
any object providing the required API. The simplest possible DOM
node is the following::

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

With a compliant DOM node definition, you can create an instance of the DOM node class and query the layout that results::

    >>> from colosseum import CSS
    >>> node = MyDOMNode(style=CSS(width=1000, height=1000))
    >>> node.add(MyDOMNode(style=CSS(width=100, height=200)))
    >>> node.add(MyDOMNode(style=CSS(width=300, height=150)))
    >>> layout = node.layout
    >>> print(node.layout)
    <Box (1000x1000 @ 0,0)>
    >>> node.layout.content_width
    1000
    >>> node.layout.content_width
    1000
    >>> node.layout.content_top
    0
    >>> node.layout.content_left
    0
    >>> for child in node.children:
    ...     print(child.layout)
    <Box (100x200 @ 0,0)>
    <Box (300x150 @ 0,200)>

Calling ``node.style.apply()`` forces the box model to be evaluated. Once
evaluated, the layout will be cached. Modifying any CSS property on a node
will mark the layout as dirty, and calling ``apply()`` again will cause the
layout to be re-evaluated. For example, if we switch the outer node to be a
"column" flex-box, rather than a "row" flex-box, you'll see the coordinates of
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
