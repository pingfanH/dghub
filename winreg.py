HKEY_LOCAL_MACHINE = object()
HKEY_CURRENT_USER = object()
HKEY_CLASSES_ROOT = object()
KEY_READ = 0x20019
KEY_WOW64_64KEY = 0x0100
KEY_WOW64_32KEY = 0x0200


class WindowsError(OSError):
    pass


class _MissingKey:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def OpenKey(*args, **kwargs):
    return _MissingKey()


def QueryValueEx(*args, **kwargs):
    raise OSError("winreg is not available on macOS")


def EnumKey(*args, **kwargs):
    raise OSError("winreg is not available on macOS")


def EnumValue(*args, **kwargs):
    raise OSError("winreg is not available on macOS")


def CloseKey(*args, **kwargs):
    return None
