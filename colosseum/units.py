
__all__ = [
    'ch', 'cm', 'em', 'ex', 'inch', 'mm', 'pc', 'percent',
    'pt', 'px', 'vh', 'vmax', 'vmin', 'vw',
]


class Unit:
    UNITS = []

    def __init__(self, suffix, val=None):
        Unit.UNITS.append((suffix, self))
        self.suffix = suffix
        self.val = val if val else 1

    def pixels(self, display=None, font=None, size=None):
        return self.val

    def dup(self, val):
        return Unit(self.suffix, val)

    def __str__(self):
        return '{}{}'.format(self.val, self.suffix)

    def __rmul__(self, val):
        if isinstance(val, (int, float)):
            return self.dup(self.val * val)


class FontUnit(Unit):
    def pixels(self, display=None, font=None, size=None):
        return self.val * (getattr(font, self.suffix) / 72) * display.dpi

    def dup(self, val):
        return FontUnit(self.suffix, val)


class AbsoluteUnit(Unit):
    def __init__(self, suffix, scale, val=None):
        super().__init__(suffix, val)
        self.scale = scale

    def pixels(self, display=None, font=None, size=None):
        return self.val * (self.scale / 72) * display.dpi

    def dup(self, val):
        return AbsoluteUnit(self.suffix, self.scale, val)


class ViewportUnit(Unit):
    def __init__(self, suffix, scale, val=None):
        super().__init__(suffix, val)
        self.scale = scale

    def pixels(self, display=None, font=None, size=None):
        return self.val * self.scale(display) / 100

    def dup(self, val):
        return ViewportUnit(self.suffix, self.scale, val)


class Percent(Unit):
    def __init__(self, val=None):
        super().__init__('%', val)

    def pixels(self, display=None, font=None, size=None):
        return self.val / 100.0 * size

    def dup(self, val):
        return Percent(val)


px = Unit('px')

em = FontUnit('em')
ex = FontUnit('ex')
ch = FontUnit('ch')

pc = AbsoluteUnit('pc', 6)
pt = AbsoluteUnit('pt', 1)
inch = AbsoluteUnit('in', 72)
cm = AbsoluteUnit('cm', 28.3465)
mm = AbsoluteUnit('mm', 2.83465)

vh = ViewportUnit('vh', lambda d: d.height)
vmax = ViewportUnit('vmax', lambda d: max(d.width, d.height))
vmin = ViewportUnit('vmin', lambda d: min(d.width, d.height))
vw = ViewportUnit('vw', lambda d: d.width)

percent = Percent()
