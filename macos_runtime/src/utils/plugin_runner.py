# Source Generated with Decompyle++
# File: plugin_runner.pyc (Python 3.11)

'''在打包后的主程序 EXE 内运行外部插件 entry（.py），避免再起一个桌面窗口。'''
from __future__ import annotations
import runpy
import sys
from pathlib import Path

def run_plugin_script(script_path = None):
    '''以 __main__ 执行插件脚本后退出进程（供 --plugin-runner 子进程模式）。'''
    path = Path(script_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f'''插件 entry 不存在: {path}''')
    sys.argv = [
        str(path)]
    runpy.run_path(str(path), run_name = '__main__')
    sys.exit(0)

