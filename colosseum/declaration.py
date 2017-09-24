from . import engine as css_engine
from .constants import (
    AUTO, INLINE, STATIC, DISPLAY_CHOICES, POSITION_CHOICES, FLOAT_CHOICES, CLEAR_CHOICES,
)
from .units import Unit


_CSS_PROPERTIES = set()


def dirty_property(name, choices=None, default=None):
    "Define a simple CSS property attribute."
    def getter(self):
        return getattr(self, '_%s' % name, default)

    def setter(self, value):
        if value != getattr(self, '_%s' % name, default):
            if choices and value not in choices:
                raise ValueError("Invalid value '%s' for CSS property '%s'; Valid values are: %s" % (
                    value,
                    name,
                    ', '.join(sorted(str(s).replace('_', '-') for s in choices)))
                )
            setattr(self, '_%s' % name, value)
            self.dirty = True

    def deleter(self):
        try:
            delattr(self, '_%s' % name)
            self.dirty = True
        except AttributeError:
            # Attribute doesn't exist
            pass

    _CSS_PROPERTIES.add(name)
    return property(getter, setter, deleter)


def directional_property(name, default=0):
    "Define a property attribute that proxies for top/right/bottom/left alternatives."
    def getter(self):
        return (
            getattr(self, name % '_top', default),
            getattr(self, name % '_right', default),
            getattr(self, name % '_bottom', default),
            getattr(self, name % '_left', default),
        )

    def setter(self, value):
        try:
            if len(value) == 4:
                setattr(self, name % '_top', value[0])
                setattr(self, name % '_right', value[1])
                setattr(self, name % '_bottom', value[2])
                setattr(self, name % '_left', value[3])
            elif len(value) == 3:
                setattr(self, name % '_top', value[0])
                setattr(self, name % '_right', value[1])
                setattr(self, name % '_bottom', value[2])
                setattr(self, name % '_left', value[1])
            elif len(value) == 2:
                setattr(self, name % '_top', value[0])
                setattr(self, name % '_right', value[1])
                setattr(self, name % '_bottom', value[0])
                setattr(self, name % '_left', value[1])
            elif len(value) == 1:
                setattr(self, name % '_top', value[0])
                setattr(self, name % '_right', value[0])
                setattr(self, name % '_bottom', value[0])
                setattr(self, name % '_left', value[0])
            else:
                raise ValueError("Invalid value for '%s'; value must be an number, or a 1-4 tuple." % (name % ''))
        except TypeError:
            setattr(self, name % '_top', value)
            setattr(self, name % '_right', value)
            setattr(self, name % '_bottom', value)
            setattr(self, name % '_left', value)

    def deleter(self):
        delattr(self, name % '_top')
        delattr(self, name % '_right')
        delattr(self, name % '_bottom')
        delattr(self, name % '_left')

    _CSS_PROPERTIES.add(name % '')
    _CSS_PROPERTIES.add(name % '_top')
    _CSS_PROPERTIES.add(name % '_right')
    _CSS_PROPERTIES.add(name % '_bottom')
    _CSS_PROPERTIES.add(name % '_left')
    return property(getter, setter, deleter)


def render_value(val):
    if isinstance(val, int):
        return '%spx' % val
    else:
        return str(val)


class CSS:
    def __init__(self, **style):
        self._node = None
        self.set(**style)

    ######################################################################
    # Style properties
    ######################################################################

    width = dirty_property('width', default=AUTO)
    height = dirty_property('height', default=AUTO)

    min_width = dirty_property('min_width', default=0)
    min_height = dirty_property('min_height', default=0)
    max_width = dirty_property('max_width')
    max_height = dirty_property('max_height')

    display = dirty_property('display', choices=DISPLAY_CHOICES, default=INLINE)
    position = dirty_property('position', choices=POSITION_CHOICES, default=STATIC)
    # float_ = dirty_property('float', choices=FLOAT_CHOICES, default=None)
    clear = dirty_property('clear', choices=CLEAR_CHOICES, default=None)

    top = dirty_property('top', default=AUTO)
    bottom = dirty_property('bottom', default=AUTO)
    left = dirty_property('left', default=AUTO)
    right = dirty_property('right', default=AUTO)

    margin_top = dirty_property('margin_top', default=0)
    margin_right = dirty_property('margin_right', default=0)
    margin_bottom = dirty_property('margin_bottom', default=0)
    margin_left = dirty_property('margin_left', default=0)

    padding_top = dirty_property('padding_top', default=0)
    padding_right = dirty_property('padding_right', default=0)
    padding_bottom = dirty_property('padding_bottom', default=0)
    padding_left = dirty_property('padding_left', default=0)

    border_top_width = dirty_property('border_top_width', default=0)
    border_right_width = dirty_property('border_right_width', default=0)
    border_bottom_width = dirty_property('border_bottom_width', default=0)
    border_left_width = dirty_property('border_left_width', default=0)

    # Some special case meta-properties that proxy to
    # underlying top/bottom/left/right base properties
    margin = directional_property('margin%s', default=0)
    padding = directional_property('padding%s', default=0)
    border_width = directional_property('border%s_width', default=0)

    ######################################################################
    # Proxy the dirtiness state of layout calculations
    ######################################################################
    @property
    def dirty(self):
        return self._node.layout.dirty

    @dirty.setter
    def dirty(self, value):
        self._node.layout.dirty = value

    ######################################################################
    # Obtain the layout module
    ######################################################################
    def engine(self):
        return css_engine

    ######################################################################
    # Style manipulation
    ######################################################################
    def set(self, **styles):
        "Set multiple styles on the CSS definition."
        for name, value in styles.items():
            if not hasattr(self, name):
                raise NameError("Unknown CSS style '%s'" % name)

            if value is None:
                delattr(self, name)
            else:
                setattr(self, name, value)

    def copy(self, node=None):
        "Create a duplicate of this style declaration."
        dup = CSS()
        for style in _CSS_PROPERTIES:
            setattr(dup, style, getattr(self, style))
        dup._node = node
        return dup

    ######################################################################
    # Get the rendered form of the style declaration
    ######################################################################
    def __str__(self):
        non_default = []
        for name in _CSS_PROPERTIES:
            try:
                non_default.append((
                    name.replace('_', '-'),
                    render_value(getattr(self, '_%s' % name))
                ))
            except AttributeError:
                pass

        return "; ".join(
            "%s: %s" % (name, value)
            for name, value in sorted(non_default)
        )
