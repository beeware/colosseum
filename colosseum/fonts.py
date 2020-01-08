"""Font utilities."""

import os
import sys

from .exceptions import ValidationError


class FontDatabase:
    """
    Provide information about the fonts available in the underlying system.
    """
    _FONTS_CACHE = {}

    @classmethod
    def validate_font_family(cls, value):
        """
        Validate a font family with the system found fonts.

        Found fonts are cached for future usage.
        """
        if value in cls._FONTS_CACHE:
            return value
        else:
            if check_font_family(value):
                # TODO: to be filled with a font properties instance
                cls._FONTS_CACHE[value] = None
                return value

        raise ValidationError('Font family "{value}" not found on system!'.format(value=value))


def _check_font_family_mac(value):
    """List available font family names on mac."""
    from ctypes import cdll, util
    from rubicon.objc import ObjCClass
    appkit = cdll.LoadLibrary(util.find_library('AppKit'))  # noqa
    NSFontManager = ObjCClass("NSFontManager")
    NSFontManager.declare_class_property('sharedFontManager')
    NSFontManager.declare_property("availableFontFamilies")
    manager = NSFontManager.sharedFontManager
    for item in manager.availableFontFamilies:
        font_name = str(item)
        if font_name == value:
            return True

    return False


def _check_font_family_unix(value):
    """List available font family names on unix."""
    import subprocess
    proc = subprocess.check_output(['fc-list', ':', 'family'])
    fonts = proc.decode().split('\n')
    for font_name in fonts:
        if font_name == value:
            return True

    return False


def _check_font_family_win(value):
    """List available font family names on windows."""
    import winreg
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                         r"Software\Microsoft\Windows NT\CurrentVersion\Fonts",
                         0,
                         winreg.KEY_READ)
    for idx in range(0, winreg.QueryInfoKey(key)[1]):
        font_name = winreg.EnumValue(key, idx)[0]
        font_name = font_name.replace(' (TrueType)', '')
        if font_name == value:
            return True

    return False


def check_font_family(value):
    """List available font family names."""
    if sys.platform == 'darwin':
        return _check_font_family_mac(value)
    elif sys.platform.startswith('linux'):
        return _check_font_family_unix(value)
    elif os.name == 'nt':
        return _check_font_family_mac(value)


def get_system_font(keyword):
    """Return a font object from given system font keyword."""
    from .constants import SYSTEM_FONT_KEYWORDS

    if keyword in SYSTEM_FONT_KEYWORDS:
        # Get the system font
        return 'Ahem'

    return None
