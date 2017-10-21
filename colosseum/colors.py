
class Color:
    pass


class rgb(Color):
    "A representation of an RGBA color"
    def __init__(self, r, g, b, a=1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __repr__(self):
        return "rgba({}, {}, {}, {})".format(self.r, self.g, self.b, self.a)

    @property
    def rgb(self):
        return self


class hsl(Color):
    "A representation of an HSLA color"
    def __init__(self, h, s, l, a=1.0):
        self.h = h
        self.s = s
        self.l = l
        self.a = a

    def __repr__(self):
        return "hsla({}, {}, {}, {})".format(self.h, self.s, self.l, self.a)

    @property
    def rgb(self):
        c = (1.0 - abs(2.0 * self.l - 1.0)) * self.s
        h = self.h / 60.0
        x = c * (1.0 - abs(h % 2 - 1.0))
        m = self.l - 0.5 * c

        if h < 1.0:
            r, g, b = c + m, x + m, m
        elif h < 2.0:
            r, g, b = x + m, c + m, m
        elif h < 3.0:
            r, g, b = m, c + m, x + m
        elif h < 4.0:
            r, g, b = m, x + m, c + m
        elif h < 5.0:
            r, g, b = m, x + m, c + m
        else:
            r, g, b = c + m, m, x + m

        return rgb(
            round(r * 0xff),
            round(g * 0xff),
            round(b * 0xff),
            self.a
        )


ALICEBLUE = 'aliceblue'
ANTIQUEWHITE = 'antiquewhite'
AQUA = 'aqua'
AQUAMARINE = 'aquamarine'
AZURE = 'azure'
BEIGE = 'beige'
BISQUE = 'bisque'
BLACK = 'black'
BLANCHEDALMOND = 'blanchedalmond'
BLUE = 'blue'
BLUEVIOLET = 'blueviolet'
BROWN = 'brown'
BURLYWOOD = 'burlywood'
CADETBLUE = 'cadetblue'
CHARTREUSE = 'chartreuse'
CHOCOLATE = 'chocolate'
CORAL = 'coral'
CORNFLOWERBLUE = 'cornflowerblue'
CORNSILK = 'cornsilk'
CRIMSON = 'crimson'
CYAN = 'cyan'
DARKBLUE = 'darkblue'
DARKCYAN = 'darkcyan'
DARKGOLDENROD = 'darkgoldenrod'
DARKGRAY = 'darkgray'
DARKGREY = 'darkgrey'
DARKGREEN = 'darkgreen'
DARKKHAKI = 'darkkhaki'
DARKMAGENTA = 'darkmagenta'
DARKOLIVEGREEN = 'darkolivegreen'
DARKORANGE = 'darkorange'
DARKORCHID = 'darkorchid'
DARKRED = 'darkred'
DARKSALMON = 'darksalmon'
DARKSEAGREEN = 'darkseagreen'
DARKSLATEBLUE = 'darkslateblue'
DARKSLATEGRAY = 'darkslategray'
DARKSLATEGREY = 'darkslategrey'
DARKTURQUOISE = 'darkturquoise'
DARKVIOLET = 'darkviolet'
DEEPPINK = 'deeppink'
DEEPSKYBLUE = 'deepskyblue'
DIMGRAY = 'dimgray'
DIMGREY = 'dimgrey'
DODGERBLUE = 'dodgerblue'
FIREBRICK = 'firebrick'
FLORALWHITE = 'floralwhite'
FORESTGREEN = 'forestgreen'
FUCHSIA = 'fuchsia'
GAINSBORO = 'gainsboro'
GHOSTWHITE = 'ghostwhite'
GOLD = 'gold'
GOLDENROD = 'goldenrod'
GRAY = 'gray'
GREY = 'grey'
GREEN = 'green'
GREENYELLOW = 'greenyellow'
HONEYDEW = 'honeydew'
HOTPINK = 'hotpink'
INDIANRED = 'indianred'
INDIGO = 'indigo'
IVORY = 'ivory'
KHAKI = 'khaki'
LAVENDER = 'lavender'
LAVENDERBLUSH = 'lavenderblush'
LAWNGREEN = 'lawngreen'
LEMONCHIFFON = 'lemonchiffon'
LIGHTBLUE = 'lightblue'
LIGHTCORAL = 'lightcoral'
LIGHTCYAN = 'lightcyan'
LIGHTGOLDENRODYELLOW = 'lightgoldenrodyellow'
LIGHTGRAY = 'lightgray'
LIGHTGREY = 'lightgrey'
LIGHTGREEN = 'lightgreen'
LIGHTPINK = 'lightpink'
LIGHTSALMON = 'lightsalmon'
LIGHTSEAGREEN = 'lightseagreen'
LIGHTSKYBLUE = 'lightskyblue'
LIGHTSLATEGRAY = 'lightslategray'
LIGHTSLATEGREY = 'lightslategrey'
LIGHTSTEELBLUE = 'lightsteelblue'
LIGHTYELLOW = 'lightyellow'
LIME = 'lime'
LIMEGREEN = 'limegreen'
LINEN = 'linen'
MAGENTA = 'magenta'
MAROON = 'maroon'
MEDIUMAQUAMARINE = 'mediumaquamarine'
MEDIUMBLUE = 'mediumblue'
MEDIUMORCHID = 'mediumorchid'
MEDIUMPURPLE = 'mediumpurple'
MEDIUMSEAGREEN = 'mediumseagreen'
MEDIUMSLATEBLUE = 'mediumslateblue'
MEDIUMSPRINGGREEN = 'mediumspringgreen'
MEDIUMTURQUOISE = 'mediumturquoise'
MEDIUMVIOLETRED = 'mediumvioletred'
MIDNIGHTBLUE = 'midnightblue'
MINTCREAM = 'mintcream'
MISTYROSE = 'mistyrose'
MOCCASIN = 'moccasin'
NAVAJOWHITE = 'navajowhite'
NAVY = 'navy'
OLDLACE = 'oldlace'
OLIVE = 'olive'
OLIVEDRAB = 'olivedrab'
ORANGE = 'orange'
ORANGERED = 'orangered'
ORCHID = 'orchid'
PALEGOLDENROD = 'palegoldenrod'
PALEGREEN = 'palegreen'
PALETURQUOISE = 'paleturquoise'
PALEVIOLETRED = 'palevioletred'
PAPAYAWHIP = 'papayawhip'
PEACHPUFF = 'peachpuff'
PERU = 'peru'
PINK = 'pink'
PLUM = 'plum'
POWDERBLUE = 'powderblue'
PURPLE = 'purple'
REBECCAPURPLE = 'rebeccapurple'
RED = 'red'
ROSYBROWN = 'rosybrown'
ROYALBLUE = 'royalblue'
SADDLEBROWN = 'saddlebrown'
SALMON = 'salmon'
SANDYBROWN = 'sandybrown'
SEAGREEN = 'seagreen'
SEASHELL = 'seashell'
SIENNA = 'sienna'
SILVER = 'silver'
SKYBLUE = 'skyblue'
SLATEBLUE = 'slateblue'
SLATEGRAY = 'slategray'
SLATEGREY = 'slategrey'
SNOW = 'snow'
SPRINGGREEN = 'springgreen'
STEELBLUE = 'steelblue'
TAN = 'tan'
TEAL = 'teal'
THISTLE = 'thistle'
TOMATO = 'tomato'
TURQUOISE = 'turquoise'
VIOLET = 'violet'
WHEAT = 'wheat'
WHITE = 'white'
WHITESMOKE = 'whitesmoke'
YELLOW = 'yellow'
YELLOWGREEN = 'yellowgreen'


NAMED_COLOR = {
    ALICEBLUE: rgb(0xF0, 0xF8, 0xFF),
    ANTIQUEWHITE: rgb(0xFA, 0xEB, 0xD7),
    AQUA: rgb(0x00, 0xFF, 0xFF),
    AQUAMARINE: rgb(0x7F, 0xFF, 0xD4),
    AZURE: rgb(0xF0, 0xFF, 0xFF),
    BEIGE: rgb(0xF5, 0xF5, 0xDC),
    BISQUE: rgb(0xFF, 0xE4, 0xC4),
    BLACK: rgb(0x00, 0x00, 0x00),
    BLANCHEDALMOND: rgb(0xFF, 0xEB, 0xCD),
    BLUE: rgb(0x00, 0x00, 0xFF),
    BLUEVIOLET: rgb(0x8A, 0x2B, 0xE2),
    BROWN: rgb(0xA5, 0x2A, 0x2A),
    BURLYWOOD: rgb(0xDE, 0xB8, 0x87),
    CADETBLUE: rgb(0x5F, 0x9E, 0xA0),
    CHARTREUSE: rgb(0x7F, 0xFF, 0x00),
    CHOCOLATE: rgb(0xD2, 0x69, 0x1E),
    CORAL: rgb(0xFF, 0x7F, 0x50),
    CORNFLOWERBLUE: rgb(0x64, 0x95, 0xED),
    CORNSILK: rgb(0xFF, 0xF8, 0xDC),
    CRIMSON: rgb(0xDC, 0x14, 0x3C),
    CYAN: rgb(0x00, 0xFF, 0xFF),
    DARKBLUE: rgb(0x00, 0x00, 0x8B),
    DARKCYAN: rgb(0x00, 0x8B, 0x8B),
    DARKGOLDENROD: rgb(0xB8, 0x86, 0x0B),
    DARKGRAY: rgb(0xA9, 0xA9, 0xA9),
    DARKGREY: rgb(0xA9, 0xA9, 0xA9),
    DARKGREEN: rgb(0x00, 0x64, 0x00),
    DARKKHAKI: rgb(0xBD, 0xB7, 0x6B),
    DARKMAGENTA: rgb(0x8B, 0x00, 0x8B),
    DARKOLIVEGREEN: rgb(0x55, 0x6B, 0x2F),
    DARKORANGE: rgb(0xFF, 0x8C, 0x00),
    DARKORCHID: rgb(0x99, 0x32, 0xCC),
    DARKRED: rgb(0x8B, 0x00, 0x00),
    DARKSALMON: rgb(0xE9, 0x96, 0x7A),
    DARKSEAGREEN: rgb(0x8F, 0xBC, 0x8F),
    DARKSLATEBLUE: rgb(0x48, 0x3D, 0x8B),
    DARKSLATEGRAY: rgb(0x2F, 0x4F, 0x4F),
    DARKSLATEGREY: rgb(0x2F, 0x4F, 0x4F),
    DARKTURQUOISE: rgb(0x00, 0xCE, 0xD1),
    DARKVIOLET: rgb(0x94, 0x00, 0xD3),
    DEEPPINK: rgb(0xFF, 0x14, 0x93),
    DEEPSKYBLUE: rgb(0x00, 0xBF, 0xFF),
    DIMGRAY: rgb(0x69, 0x69, 0x69),
    DIMGREY: rgb(0x69, 0x69, 0x69),
    DODGERBLUE: rgb(0x1E, 0x90, 0xFF),
    FIREBRICK: rgb(0xB2, 0x22, 0x22),
    FLORALWHITE: rgb(0xFF, 0xFA, 0xF0),
    FORESTGREEN: rgb(0x22, 0x8B, 0x22),
    FUCHSIA: rgb(0xFF, 0x00, 0xFF),
    GAINSBORO: rgb(0xDC, 0xDC, 0xDC),
    GHOSTWHITE: rgb(0xF8, 0xF8, 0xFF),
    GOLD: rgb(0xFF, 0xD7, 0x00),
    GOLDENROD: rgb(0xDA, 0xA5, 0x20),
    GRAY: rgb(0x80, 0x80, 0x80),
    GREY: rgb(0x80, 0x80, 0x80),
    GREEN: rgb(0x00, 0x80, 0x00),
    GREENYELLOW: rgb(0xAD, 0xFF, 0x2F),
    HONEYDEW: rgb(0xF0, 0xFF, 0xF0),
    HOTPINK: rgb(0xFF, 0x69, 0xB4),
    INDIANRED: rgb(0xCD, 0x5C, 0x5C),
    INDIGO: rgb(0x4B, 0x00, 0x82),
    IVORY: rgb(0xFF, 0xFF, 0xF0),
    KHAKI: rgb(0xF0, 0xE6, 0x8C),
    LAVENDER: rgb(0xE6, 0xE6, 0xFA),
    LAVENDERBLUSH: rgb(0xFF, 0xF0, 0xF5),
    LAWNGREEN: rgb(0x7C, 0xFC, 0x00),
    LEMONCHIFFON: rgb(0xFF, 0xFA, 0xCD),
    LIGHTBLUE: rgb(0xAD, 0xD8, 0xE6),
    LIGHTCORAL: rgb(0xF0, 0x80, 0x80),
    LIGHTCYAN: rgb(0xE0, 0xFF, 0xFF),
    LIGHTGOLDENRODYELLOW: rgb(0xFA, 0xFA, 0xD2),
    LIGHTGRAY: rgb(0xD3, 0xD3, 0xD3),
    LIGHTGREY: rgb(0xD3, 0xD3, 0xD3),
    LIGHTGREEN: rgb(0x90, 0xEE, 0x90),
    LIGHTPINK: rgb(0xFF, 0xB6, 0xC1),
    LIGHTSALMON: rgb(0xFF, 0xA0, 0x7A),
    LIGHTSEAGREEN: rgb(0x20, 0xB2, 0xAA),
    LIGHTSKYBLUE: rgb(0x87, 0xCE, 0xFA),
    LIGHTSLATEGRAY: rgb(0x77, 0x88, 0x99),
    LIGHTSLATEGREY: rgb(0x77, 0x88, 0x99),
    LIGHTSTEELBLUE: rgb(0xB0, 0xC4, 0xDE),
    LIGHTYELLOW: rgb(0xFF, 0xFF, 0xE0),
    LIME: rgb(0x00, 0xFF, 0x00),
    LIMEGREEN: rgb(0x32, 0xCD, 0x32),
    LINEN: rgb(0xFA, 0xF0, 0xE6),
    MAGENTA: rgb(0xFF, 0x00, 0xFF),
    MAROON: rgb(0x80, 0x00, 0x00),
    MEDIUMAQUAMARINE: rgb(0x66, 0xCD, 0xAA),
    MEDIUMBLUE: rgb(0x00, 0x00, 0xCD),
    MEDIUMORCHID: rgb(0xBA, 0x55, 0xD3),
    MEDIUMPURPLE: rgb(0x93, 0x70, 0xDB),
    MEDIUMSEAGREEN: rgb(0x3C, 0xB3, 0x71),
    MEDIUMSLATEBLUE: rgb(0x7B, 0x68, 0xEE),
    MEDIUMSPRINGGREEN: rgb(0x00, 0xFA, 0x9A),
    MEDIUMTURQUOISE: rgb(0x48, 0xD1, 0xCC),
    MEDIUMVIOLETRED: rgb(0xC7, 0x15, 0x85),
    MIDNIGHTBLUE: rgb(0x19, 0x19, 0x70),
    MINTCREAM: rgb(0xF5, 0xFF, 0xFA),
    MISTYROSE: rgb(0xFF, 0xE4, 0xE1),
    MOCCASIN: rgb(0xFF, 0xE4, 0xB5),
    NAVAJOWHITE: rgb(0xFF, 0xDE, 0xAD),
    NAVY: rgb(0x00, 0x00, 0x80),
    OLDLACE: rgb(0xFD, 0xF5, 0xE6),
    OLIVE: rgb(0x80, 0x80, 0x00),
    OLIVEDRAB: rgb(0x6B, 0x8E, 0x23),
    ORANGE: rgb(0xFF, 0xA5, 0x00),
    ORANGERED: rgb(0xFF, 0x45, 0x00),
    ORCHID: rgb(0xDA, 0x70, 0xD6),
    PALEGOLDENROD: rgb(0xEE, 0xE8, 0xAA),
    PALEGREEN: rgb(0x98, 0xFB, 0x98),
    PALETURQUOISE: rgb(0xAF, 0xEE, 0xEE),
    PALEVIOLETRED: rgb(0xDB, 0x70, 0x93),
    PAPAYAWHIP: rgb(0xFF, 0xEF, 0xD5),
    PEACHPUFF: rgb(0xFF, 0xDA, 0xB9),
    PERU: rgb(0xCD, 0x85, 0x3F),
    PINK: rgb(0xFF, 0xC0, 0xCB),
    PLUM: rgb(0xDD, 0xA0, 0xDD),
    POWDERBLUE: rgb(0xB0, 0xE0, 0xE6),
    PURPLE: rgb(0x80, 0x00, 0x80),
    REBECCAPURPLE: rgb(0x66, 0x33, 0x99),
    RED: rgb(0xFF, 0x00, 0x00),
    ROSYBROWN: rgb(0xBC, 0x8F, 0x8F),
    ROYALBLUE: rgb(0x41, 0x69, 0xE1),
    SADDLEBROWN: rgb(0x8B, 0x45, 0x13),
    SALMON: rgb(0xFA, 0x80, 0x72),
    SANDYBROWN: rgb(0xF4, 0xA4, 0x60),
    SEAGREEN: rgb(0x2E, 0x8B, 0x57),
    SEASHELL: rgb(0xFF, 0xF5, 0xEE),
    SIENNA: rgb(0xA0, 0x52, 0x2D),
    SILVER: rgb(0xC0, 0xC0, 0xC0),
    SKYBLUE: rgb(0x87, 0xCE, 0xEB),
    SLATEBLUE: rgb(0x6A, 0x5A, 0xCD),
    SLATEGRAY: rgb(0x70, 0x80, 0x90),
    SLATEGREY: rgb(0x70, 0x80, 0x90),
    SNOW: rgb(0xFF, 0xFA, 0xFA),
    SPRINGGREEN: rgb(0x00, 0xFF, 0x7F),
    STEELBLUE: rgb(0x46, 0x82, 0xB4),
    TAN: rgb(0xD2, 0xB4, 0x8C),
    TEAL: rgb(0x00, 0x80, 0x80),
    THISTLE: rgb(0xD8, 0xBF, 0xD8),
    TOMATO: rgb(0xFF, 0x63, 0x47),
    TURQUOISE: rgb(0x40, 0xE0, 0xD0),
    VIOLET: rgb(0xEE, 0x82, 0xEE),
    WHEAT: rgb(0xF5, 0xDE, 0xB3),
    WHITE: rgb(0xFF, 0xFF, 0xFF),
    WHITESMOKE: rgb(0xF5, 0xF5, 0xF5),
    YELLOW: rgb(0xFF, 0xFF, 0x00),
    YELLOWGREEN: rgb(0x9A, 0xCD, 0x32),
}
