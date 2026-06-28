# Source Generated with Decompyle++
# File: protocol.pyc (Python 3.11)

'''DGHub 插件协议消息类型。

通信传输：WebSocket，JSON 文本帧。每条消息根包含 ``op`` 字段做 discriminator。

约束：
- 消息字段命名一律 snake_case，避免跨语言客户端的歧义。
- 不允许额外字段（``extra="forbid"``）—— 早期发现协议拼写错误，避免悄悄丢字段。
- 所有强度值 / 百分比统一用 ``pct`` 字段（int，范围 0-100），不传设备原始 max 值。

兼容性：
- ``SDK_VERSION`` 采用语义化主版本号。Major 升级表示 break change，
  主程序拒绝低主版本的握手；Minor / Patch 兼容。
'''
from __future__ import annotations
from typing import Annotated, Any, Literal, Union
from pydantic import BaseModel, ConfigDict, Field
SDK_VERSION = '1.0.0'
SDK_MAJOR = 1

class PluginConfigField(BaseModel):
    '''前端通用渲染器消费的字段定义。

    type 决定 UI 控件：
      - ``percent``: 0-100 滑块（min/max 可覆盖，默认 0-100）
      - ``duration``: 浮点数字框，单位秒
      - ``number``: 通用数字框，支持 min/max/step
      - ``bool``: 开关
      - ``text``: 单行文本
      - ``select``: 下拉，options=[{"value","label"}]
      - ``preset``: 波形预设下拉（前端自动拉 preset_manager 列表）
      - ``channel``: a/b/both 三选
      - ``path``: 路径选择（dir/file）
      - ``event_table``: 复杂事件触发表（B 站礼物映射风格，schema 由插件自描述）
    '''
    model_config = ConfigDict(extra = 'forbid')
    type: "Literal['percent', 'duration', 'number', 'bool', 'text', 'select', 'preset', 'channel', 'path', 'event_table']" = Field(..., description = '存储到 config.plugins.{plugin_id}.{key}')
    label: 'str' = Field(..., description = 'UI 显示的字段名')
    default: 'Any' = None
    description: 'str | None' = None
    min: 'float | None' = None
    max: 'float | None' = None
    step: 'float | None' = None
    options: 'list[dict[str, Any]] | None' = None
    path_kind: "Literal['file', 'dir'] | None" = None
    row_schema: "list['PluginConfigField'] | None" = None


class PluginConfigSection(BaseModel):
    '''配置分组（一张卡片对应一个 section）'''
    model_config = ConfigDict(extra = 'forbid')
    fields: 'list[PluginConfigField]' = Field(..., description = "分组标题，如 '基础' / '事件' / '高级'")


class PluginManifest(BaseModel):
    '''插件包根目录下的 manifest.json 内容。'''
    model_config = ConfigDict(extra = 'forbid')
    id: 'str' = Field(..., pattern = '^[a-z][a-z0-9_-]{1,31}$', description = '唯一标识，2-32 字符，小写字母/数字/_/-')
    name: 'str' = Field(..., description = "显示名，例：'我的游戏联动'")
    version: 'str' = Field(..., description = "语义化版本，例：'0.1.0'")
    sdk: 'str' = Field(..., description = "所兼容的 SDK 主版本，例：'1'")
    author: 'str | None' = None
    description: 'str | None' = None
    homepage: 'str | None' = None
    entry: 'str | None' = Field(None, description = '可执行文件相对路径；若为 None 则插件须由用户手动启动')
    config_schema: 'list[PluginConfigSection] | None' = None


class _BaseMsg(BaseModel):
    model_config = ConfigDict(extra = 'forbid')


class HelloMsg(_BaseMsg):
    op: Literal['hello'] = 'hello'
    manifest: 'PluginManifest' = '握手 — 插件连接后第一条必须发的消息。'
    token: 'str' = Field(..., description = '启动时主程序通过 --token 传入')


class EventMsg(_BaseMsg):
    op: Literal['event'] = 'event'
    label: 'str' = Field(..., description = "事件类型，例：'受击' / '弹幕命中'")
    name: 'str' = Field(..., description = "事件具体内容，例：'BOSS 重击 -25HP' / 弹幕原文")
    username: 'str' = Field('', description = '可选，触发者，例：直播观众昵称')
    cause: 'str' = Field('', description = '触发原因人话句，供悬浮窗按因果显示')
    pulse_name: 'str' = Field('', description = '本次事件实际使用的波形预设名')
    strength_pct: 'int | None' = Field(None, ge = 0, le = 100, description = '兼容旧字段；等价 ``to_pct``')
    from_pct: 'int | None' = Field(None, ge = 0, le = 100, description = '事件前 baseline 百分比')
    to_pct: 'int | None' = Field(None, ge = 0, le = 100, description = '事件后目标百分比')
    delta_pct: 'int | None' = Field(None, ge = -200, le = 200, description = 'to_pct - from_pct')
    duration: 'float' = Field(1, ge = 0, description = '事件展示时长 / 波形持续时间（秒）')
    event_id: 'str | None' = None


class PulseMsg(_BaseMsg):
    op: Literal['pulse'] = 'pulse'
    preset: 'str' = Field(..., description = '波形预设名称')
    channel: "Literal['a', 'b', 'both']" = 'both'


class SetStrengthMsg(_BaseMsg):
    op: Literal['set_strength'] = 'set_strength'
    channel: "Literal['a', 'b', 'both']" = '绝对设置该插件的强度层（百分比）。'
    pct: 'int' = Field(..., ge = 0, le = 100)


class AdjustStrengthMsg(_BaseMsg):
    op: Literal['adjust_strength'] = 'adjust_strength'
    channel: "Literal['a', 'b', 'both']" = '增减该插件的强度层（正负百分比）。'
    delta_pct: 'int' = Field(..., ge = -100, le = 100)


class TriggerMsg(_BaseMsg):
    op: Literal['trigger'] = 'trigger'
    action: "Literal['both', 'strength', 'waveform']" = Field('both', description = 'both=同时改强度+播波形；strength=只改强度；waveform=只播波形')
    delta_pct: 'int' = Field(0, ge = -100, le = 100, description = '相对插件当前 baseline 的增量百分比（可正负），action=waveform 时忽略')
    strength_mode: "Literal['rollback', 'permanent']" = Field('rollback', description = 'rollback=duration 后回正；permanent=直接修改插件 baseline')
    duration_s: 'float' = Field(1, ge = 0, le = 300, description = '波形播放时长 + rollback 模式下的强度保持时长')
    preset: 'str | None' = Field(None, description = '波形预设名称，action 含 waveform 时必填')
    channel: "Literal['a', 'b', 'both']" = 'both'
    label: 'str' = Field('', description = 'UI 显示用的事件标签（类型，如「受击」/「弹幕命中」）')
    username: 'str' = Field('', description = 'UI 显示用的触发者')
    name: 'str' = Field('', description = 'UI 显示用的具体内容（弹幕原文 / 礼物名 / 击杀者）')
    cause: 'str' = Field('', description = '触发原因人话句，供悬浮窗按因果显示')
    pulse_name: 'str | None' = Field(None, description = '兼容字段：若想强制覆盖事件流里显示的波形名（一般不需要，默认用 preset）')


class StatusMsg(_BaseMsg):
    op: Literal['status'] = 'status'
    fields: 'dict[str, Any]' = Field(default_factory = dict)


class LogMsg(_BaseMsg):
    op: Literal['log'] = 'log'
    message: 'str' = 'info'


class SetConfigMsg(_BaseMsg):
    op: Literal['set_config'] = 'set_config'
    key: 'str'
    value: 'Any' = "插件主动修改自己的配置项（持久化到 config.json）。\n\n    例：插件想记录 'total_runs' / 'last_save_path' 等运行时计数。\n    用户通过前端改的配置，主程序会主动推 ConfigChangedMsg 给插件，\n    不需要插件自己 set。\n    "

ClientMsg = Annotated[(Union[(HelloMsg, TriggerMsg, EventMsg, PulseMsg, SetStrengthMsg, AdjustStrengthMsg, StatusMsg, LogMsg, SetConfigMsg)], Field(discriminator = 'op'))]

class HelloAckMsg(_BaseMsg):
    op: Literal['hello_ack'] = 'hello_ack'
    accepted: 'bool' = SDK_VERSION
    reason: 'str | None' = Field(None, description = '未通过时的拒绝原因')


class ConfigMsg(_BaseMsg):
    op: Literal['config'] = 'config'
    data: 'dict[str, Any]' = '全量推送当前配置 — 握手后立刻发一次，之后只发 ConfigChangedMsg。'


class ConfigChangedMsg(_BaseMsg):
    op: Literal['config_changed'] = 'config_changed'
    key: 'str'
    value: 'Any' = '单字段变更 — 用户在前端改了配置。'


class DeviceInfoMsg(_BaseMsg):
    op: Literal['device_info'] = 'device_info'
    connected: 'bool' = '设备状态推送 — 连接 / 断开 / max 强度变化时下发。'
    device_type: 'str' = Field('', description = "v2 / v3 / ''")
    max_strength_a: 'int' = 0
    max_strength_b: 'int' = 0


class StopMsg(_BaseMsg):
    op: "Literal['stop']" = '主程序通知插件优雅停止 — 插件收到后应清理资源并关闭 WS 连接。'
    reason: 'str' = ''


class PingMsg(_BaseMsg):
    op: "Literal['ping']" = '主程序保活探测。'
    t: 'float' = Field(..., description = '发送时间戳（秒）')


class PongMsg(_BaseMsg):
    op: Literal['pong'] = 'pong'
    t: 'float' = '插件响应保活。'

ServerMsg = Annotated[(Union[(HelloAckMsg, ConfigMsg, ConfigChangedMsg, DeviceInfoMsg, StopMsg, PingMsg, PongMsg)], Field(discriminator = 'op'))]
PluginConfigField.model_rebuild()
