# Source Generated with Decompyle++
# File: single_instance.pyc (Python 3.11)

'''桌面主程序单实例：重复启动时激活已有窗口并退出。'''
from __future__ import annotations
import sys
from src.utils.logger import get_logger
logger = get_logger('SingleInstance')
_MUTEX_NAME = 'Global\\DGHub_Desktop_SingleInstance_v1'
_WINDOW_TITLE = 'DGHub'

def _activate_existing_window():
    if sys.platform != 'win32':
        return False
    
    try:
        import ctypes
        user32 = ctypes.windll.user32
        hwnd = user32.FindWindowW(None, _WINDOW_TITLE)
        if not hwnd:
            return False
        SW_RESTORE = None
        user32.ShowWindow(hwnd, SW_RESTORE)
        user32.SetForegroundWindow(hwnd)
        return True
    except Exception:
        e = None
        logger.debug(f'''激活已有窗口失败: {e}''')
        e = None
        del e
        return False
        e = None
        del e



def try_acquire_desktop_instance():
    '''尝试成为唯一桌面实例。若已有实例在运行则激活其窗口并返回 False。'''
    if sys.platform != 'win32':
        return True
    
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        ERROR_ALREADY_EXISTS = 183
        handle = kernel32.CreateMutexW(None, False, _MUTEX_NAME)
        if not handle:
            return True
        if None.GetLastError() == ERROR_ALREADY_EXISTS:
            kernel32.CloseHandle(handle)
            if _activate_existing_window():
                logger.info('已有 DGHub 在运行，已激活前台窗口')
            else:
                logger.info('已有 DGHub 在运行（未能定位窗口）')
            return False
        return None
    except Exception:
        e = None
        logger.warning(f'''单实例互斥创建失败，允许多开: {e}''')
        e = None
        del e
        return True
        e = None
        del e


