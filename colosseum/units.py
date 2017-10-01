
__all__ = [
    'ch', 'cm', 'em', 'ex', 'inch', 'mm', 'pc', 'percent',
    'pt', 'px', 'vh', 'vmax', 'vmin', 'vw',
]

LU_PER_PIXEL = 64


class Unit:
    UNITS = []

    def __init__(self, suffix, val=None):
        Unit.UNITS.append((suffix, self))
        self.suffix = suffix
        self.val = val if val is not None else 1

    def lu(self, display=None, font=None, size=None):
        return round(LU_PER_PIXEL * self.val)

    def px(self, display=None, font=None, size=None):
        return self.lu(display=display, font=font, size=size) // LU_PER_PIXEL

    def __repr__(self):
        return '{}{}'.format(self.val, self.suffix)

    def __str__(self):
        return '{}{}'.format(self.val, self.suffix)

    def __rmul__(self, val):
        if isinstance(val, (int, float)):
            return self.dup(self.val * val)


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

pc = AbsoluteUnit('pc', 6)
pt = AbsoluteUnit('pt', 1)
inch = AbsoluteUnit('in', 72)
cm = AbsoluteUnit('cm', 28.3465)
mm = AbsoluteUnit('mm', 2.83465)

vh = ViewportUnit('vh', lambda d: d.content_height)
vmax = ViewportUnit('vmax', lambda d: max(d.content_width, d.content_height))
vmin = ViewportUnit('vmin', lambda d: min(d.content_width, d.content_height))
vw = ViewportUnit('vw', lambda d: d.content_width)

percent = Percent()
