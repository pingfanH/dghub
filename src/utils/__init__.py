# Source Generated with Decompyle++
# File: __init__.pyc (Python 3.11)

'''公共工具函数'''
from src.utils.network import get_local_ip, get_network_interfaces, get_local_ip_by_interface
from src.utils.qrcode import generate_qrcode
from src.utils.cs2_path import find_cs2_install_path, setup_cs2_gamestate_cfg
import os
import sys

def get_resource_path(relative_path = None):
    '''获取资源文件的绝对路径（兼容 PyInstaller 打包）'''
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

__all__ = [
    'get_resource_path',
    'get_local_ip',
    'get_network_interfaces',
    'get_local_ip_by_interface',
    'generate_qrcode',
    'find_cs2_install_path',
    'setup_cs2_gamestate_cfg']
