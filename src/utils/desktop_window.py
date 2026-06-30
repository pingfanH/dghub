# Source Generated with Decompyle++
# File: desktop_window.pyc (Python 3.11)

'''pywebview 主窗口操作（从 routes 拆出，避免 routes 内联 import 触发类型检查告警）。'''
import threading

def minimize_main_window():
    
    try:
        import webview
    except ImportError:
        return False

    if webview.windows:
        webview.windows[0].minimize()
        return True


def close_main_window():
    '''标记确认退出并延迟 destroy，避免 HTTP 线程与 GUI 消息泵死锁。'''
    
    try:
        import webview
    except ImportError:
        return False

    if not webview.windows:
        return False
    
    try:
        set_exit_confirmed = set_exit_confirmed
        import src.runtime_flags
        set_exit_confirmed()
    except Exception:
        pass

    win = webview.windows[0]
    threading.Timer(0.05, win.destroy).start()
    return True

