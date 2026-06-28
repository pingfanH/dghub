# Source Generated with Decompyle++
# File: runtime_flags.pyc (Python 3.11)

"""跨模块共享的运行时标志位。

⚠️ 为什么单独放一个模块：PyInstaller 打包后 src/main.py 作为入口运行，
sys.modules 里同时存在 '__main__' 和（被 src.api.routes 二次 import 的）'src.main' 两份。
模块级变量在两份里各有一份，任何一边写都不会同步到另一边——这正是 1.2.4 / 1.2.5 关闭未响应的根因。

把状态放在一个**绝不会被作为入口运行**的小模块里，无论谁 import 都拿到同一份。
"""
_exit_confirmed = False

def set_exit_confirmed():
    '''供 API 层调用：标记用户已经确认退出，下一次 closing 事件直接放行。'''
    global _exit_confirmed
    _exit_confirmed = True


def is_exit_confirmed():
    return _exit_confirmed

