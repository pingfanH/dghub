# Source Generated with Decompyle++
# File: plugin_assets.pyc (Python 3.11)

'''外部插件相关静态资源路径（开发文档、示范插件）。'''
from __future__ import annotations
import os
import tempfile
import zipfile
from pathlib import Path
from src.utils import get_resource_path

def dev_guide_path():
    candidates = [
        Path(get_resource_path('docs/PLUGIN_DEVELOPMENT.md')),
        Path(__file__).resolve().parents[2] / 'docs' / 'PLUGIN_DEVELOPMENT.md']
    for p in candidates:
        if p.is_file():
            
            return None, p
        return candidates[0]


def demo_external_dir():
    candidates = [
        Path(get_resource_path('plugins/demo_external')),
        Path(__file__).resolve().parents[2] / 'plugins' / 'demo_external']
    for p in candidates:
        if p.is_dir() and (p / 'manifest.json').is_file():
            
            return None, p
        return None


def build_demo_zip_file():
    '''写入临时 zip，返回 (路径, 是否需在完成后删除)。

    Raises:
        FileNotFoundError: 示范插件目录不存在
        OSError: 临时文件或写入 zip 失败（磁盘满、权限等）
    '''
    demo_dir = demo_external_dir()
# WARNING: Decompyle incomplete


def demo_zip_pack_error_message(exc = None):
    '''将 build_demo_zip_file 异常转为面向用户的简短说明。'''
    if isinstance(exc, FileNotFoundError):
        return '示范插件未找到'
    if None(exc, OSError):
        return f'''打包示范插件失败：{exc}'''

