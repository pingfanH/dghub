# Source Generated with Decompyle++
# File: deps.pyc (Python 3.11)

'''API 层共享依赖（避免 routes 子模块互相 import 主 routes）。'''
from src.config.config_manager import ConfigManager

def get_config():
    from src.api.app import config
    return config


def get_preset_mgr():
    from src.api.app import preset_manager
    return preset_manager
