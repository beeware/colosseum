import math

__all__ = [
    'ch', 'cm', 'em', 'ex', 'inch', 'mm', 'pc', 'percent',
    'pt', 'px', 'vh', 'vmax', 'vmin', 'vw', 'deg', 'rad',
    'grad', 'turn',
]

LU_PER_PIXEL = 64


class BaseUnit:
    UNITS = []

    def __init__(self, suffix, val=None):
        BaseUnit.UNITS.append((suffix, self))
        self.suffix = suffix
        self.val = val if val is not None else 1

    def __repr__(self):
        int_value = int(self.val)
        value = int_value if self.val == int_value else self.val
        return '{}{}'.format(value, self.suffix)

    def __str__(self):
        int_value = int(self.val)
        value = int_value if self.val == int_value else self.val
        return '{}{}'.format(value, self.suffix)

    def __rmul__(self, val):
        if isinstance(val, (int, float)):
            return self.dup(self.val * val)

    def __neg__(self):
        if isinstance(self.val, int):
            return self.dup(self.val * -1)
        elif isinstance(self.val, float):
            return self.dup(self.val * -1.0)


class Unit(BaseUnit):

    def lu(self, display=None, font=None, size=None):
        return round(LU_PER_PIXEL * self.val)

    def px(self, display=None, font=None, size=None):
        logical_units = self.lu(display=display, font=font, size=size)
        value = logical_units / LU_PER_PIXEL
        int_value = int(value)
        return int_value if value == int_value else value


class AngleUnit(BaseUnit):
    def __init__(self, suffix, scale, val=None):
        super().__init__(suffix, val)
        self.scale = scale

    def deg(self):
        value = self.val * self.scale
        value_int = int(value)
        return value_int if value == value_int else value

    def dup(self, val):
        return AngleUnit(self.suffix, self.scale, val)

    def __eq__(self, other):
        if isinstance(other, AngleUnit):
            return self.val == other.val and self.suffix == other.suffix
        return False


class PixelUnit(Unit):
    def __init__(self, val=None):
        super().__init__('px', val)

    def dup(self, val):
        return PixelUnit(val)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.val == other
        elif isinstance(other, PixelUnit):
            return self.val == other.val
        return False


class FontUnit(Unit):
    def lu(self, display=None, font=None, size=None):
        return round(LU_PER_PIXEL * self.val * (getattr(font, self.suffix) / 72) * display.dpi)

    def dup(self, val):
        return FontUnit(self.suffix, val)

    def __eq__(self, other):
        if isinstance(other, FontUnit):
            return self.val == other.val and self.suffix == other.suffix
        return False


class AbsoluteUnit(Unit):
    def __init__(self, suffix, scale, val=None):
        super().__init__(suffix, val)
        self.scale = scale

    def lu(self, display=None, font=None, size=None):
        return round(LU_PER_PIXEL * self.val * (self.scale / 72) * display.dpi)

    def dup(self, val):
        return AbsoluteUnit(self.suffix, self.scale, val)

    def __eq__(self, other):
        if isinstance(other, AbsoluteUnit):
            return self.val == other.val and self.suffix == other.suffix
        return False


class ViewportUnit(Unit):
    def __init__(self, suffix, scale, val=None):
        super().__init__(suffix, val)
        self.scale = scale

    def lu(self, display=None, font=None, size=None):
        return round(LU_PER_PIXEL * self.val * self.scale(display) / 100)

    def dup(self, val):
        return ViewportUnit(self.suffix, self.scale, val)

    def __eq__(self, other):
        if isinstance(other, ViewportUnit):
            return self.val == other.val and self.suffix == other.suffix
        return False


class Percent(Unit):
    def __init__(self, val=None):
        super().__init__('%', val)

    def lu(self, display=None, font=None, size=None):
        return round(LU_PER_PIXEL * self.val / 100.0 * size)

    def dup(self, val):
        return Percent(val)

    def __eq__(self, other):
        if isinstance(other, Percent):
            return self.val == other.val and self.suffix == other.suffix
        return False


px = PixelUnit()

em = FontUnit('em')
ex = FontUnit('ex')
ch = FontUnit('ch')

pt = AbsoluteUnit('pt', 1)
pc = AbsoluteUnit('pc', 12)
inch = AbsoluteUnit('in', 72)
cm = AbsoluteUnit('cm', 28.3465)
mm = AbsoluteUnit('mm', 2.83465)

vh = ViewportUnit('vh', lambda d: d.content_height)
vmax = ViewportUnit('vmax', lambda d: max(d.content_width, d.content_height))
vmin = ViewportUnit('vmin', lambda d: min(d.content_width, d.content_height))
vw = ViewportUnit('vw', lambda d: d.content_width)

percent = Percent()

deg = AngleUnit('deg', 1)
grad = AngleUnit('grad', 0.9)
rad = AngleUnit('rad', 180/math.pi)
turn = AngleUnit('turn', 360)
