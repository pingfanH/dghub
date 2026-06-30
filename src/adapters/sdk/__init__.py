# Source Generated with Decompyle++
# File: __init__.pyc (Python 3.11)

'''DGHub 插件 SDK — 用于第三方插件 / 内置 RemoteAdapter 之间共享的协议类型。

第三方插件作者请引用 ``protocol`` 子模块：
    from src.adapters.sdk.protocol import PluginManifest, ClientMsg, ServerMsg

协议版本号在 ``SDK_VERSION``；插件 manifest 中应声明所兼容的 SDK 主版本（``sdk``）。
'''
from src.adapters.sdk.protocol import SDK_VERSION, PluginManifest, PluginConfigField, PluginConfigSection, ClientMsg, HelloMsg, EventMsg, PulseMsg, SetStrengthMsg, AdjustStrengthMsg, StatusMsg, LogMsg, SetConfigMsg, ServerMsg, HelloAckMsg, ConfigMsg, ConfigChangedMsg, DeviceInfoMsg, StopMsg, PingMsg, PongMsg
__all__ = [
    'SDK_VERSION',
    'PluginManifest',
    'PluginConfigField',
    'PluginConfigSection',
    'ClientMsg',
    'HelloMsg',
    'EventMsg',
    'PulseMsg',
    'SetStrengthMsg',
    'AdjustStrengthMsg',
    'StatusMsg',
    'LogMsg',
    'SetConfigMsg',
    'ServerMsg',
    'HelloAckMsg',
    'ConfigMsg',
    'ConfigChangedMsg',
    'DeviceInfoMsg',
    'StopMsg',
    'PingMsg',
    'PongMsg']
