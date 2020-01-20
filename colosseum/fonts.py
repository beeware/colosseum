"""Font utilities."""

import os
import sys

from .exceptions import ValidationError


class _FontDatabaseBase:
    """
    Provide information about the fonts available in the underlying system.
    """
    _FONTS_CACHE = {}

    @classmethod
    def clear_cache(cls):
        cls._FONTS_CACHE = {}

    @classmethod
    def validate_font_family(cls, value):
        """Validate a font family with the system found fonts."""
        if value in cls._FONTS_CACHE:
            return value
        else:
            font_exists = cls.check_font_family(value)
            if font_exists:
                # TODO: to be filled with a cross-platform font properties instance
                cls._FONTS_CACHE[value] = None
                return value

        raise ValidationError('Font family "{value}" not found on system!'.format(value=value))

    @staticmethod
    def check_font_family(value):
        raise NotImplementedError()

    @staticmethod
    def fonts_path(system=False):
        """Return the path for cross platform user fonts."""
        raise NotImplementedError('System not supported!')


class _FontDatabaseMac(_FontDatabaseBase):

    @staticmethod
    def check_font_family(value):
        from ctypes import cdll, util
        from rubicon.objc import ObjCClass
        appkit = cdll.LoadLibrary(util.find_library('AppKit'))  # noqa
        NSFont = ObjCClass('NSFont')
        return bool(NSFont.fontWithName(value, size=0))  # size=0 returns defautl size

    @staticmethod
    def fonts_path(system=False):
        if system:
            fonts_dir = os.path.expanduser('/Library/Fonts')
        else:
            fonts_dir = os.path.expanduser('~/Library/Fonts')

        return fonts_dir


class _FontDatabaseWin(_FontDatabaseBase):

    @staticmethod
    def check_font_family(value):
        import winreg  # noqa

        font_name = value + ' (TrueType)'  # TODO: check other options
        font = False
        key_path = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"
        for base in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            with winreg.OpenKey(base, key_path, 0, winreg.KEY_READ) as reg_key:
                try:
                    # Query if it exists
                    font = winreg.QueryValueEx(reg_key, font_name)
                    return True
                except FileNotFoundError:
                    pass

        return font

    @staticmethod
    def fonts_path(system=False):
        import winreg
        if system:
            fonts_dir = os.path.join(winreg.ExpandEnvironmentStrings(r'%windir%'), 'Fonts')
        else:
            fonts_dir = os.path.join(winreg.ExpandEnvironmentStrings(r'%LocalAppData%'),
                                     'Microsoft', 'Windows', 'Fonts')
        return fonts_dir


class _FontDatabaseLinux(_FontDatabaseBase):
    _GTK_WINDOW = None

    @classmethod
    def check_font_family(cls, value):
        import gi  # noqa
        gi.require_version("Gtk", "3.0")
        gi.require_version("Pango", "1.0")
        from gi.repository import Gtk  # noqa
        from gi.repository import Pango  # noqa

        class Window(Gtk.Window):
            """Use Pango to get system fonts names."""

            def get_font(self, value):
                """Get font from the system."""
                context = self.create_pango_context()
                font = context.load_font(Pango.FontDescription(value))

                # Pango always loads something close to the requested so we need to check
                # the actual loaded font is the requested one.
                if font.describe().to_string().startswith(value):
                    return True  # TODO: Wrap on a font cross platform wrapper

                return False

        if cls._GTK_WINDOW is None:
            cls._GTK_WINDOW = Window()

        return cls._GTK_WINDOW.get_font(value)

    @staticmethod
    def fonts_path(system=False):
        if system:
            fonts_dir = os.path.expanduser('/usr/local/share/fonts')
        else:
            fonts_dir = os.path.expanduser('~/.local/share/fonts/')

        return fonts_dir


def get_system_font(keyword):
    """Return a font object from given system font keyword."""
    from .constants import INITIAL_FONT_VALUES, SYSTEM_FONT_KEYWORDS  # noqa

    if keyword in SYSTEM_FONT_KEYWORDS:
        # TODO: Get the system font that corresponds
        return INITIAL_FONT_VALUES.copy()

    return None


if sys.platform == 'win32':
    FontDatabase = _FontDatabaseWin
elif sys.platform == 'darwin':
    FontDatabase = _FontDatabaseMac
elif sys.platform.startswith('linux'):
    FontDatabase = _FontDatabaseLinux
else:
    raise ImportError('System not supported!')
