# Source Generated with Decompyle++
# File: events.pyc (Python 3.11)

'''Bilibili 事件类型定义 — 配置面板与运行时共用的常量'''
FRAME_MS = 100
EVENT_DEFS = {
    'danmaku': {
        'label': '弹幕关键词',
        'icon': 'comment-dots',
        'default_enabled': True,
        'default_strength': 50,
        'default_pulse': 'CS2-受伤',
        'default_action': 'both',
        'default_duration': 1,
        'default_cooldown': 0.5,
        'has_rules': True,
        'rules_type': 'keyword' },
    'gift': {
        'label': '礼物',
        'icon': 'gift',
        'default_enabled': True,
        'default_strength': 30,
        'default_pulse': 'CS2-燃烧',
        'default_action': 'both',
        'default_duration': 1.5,
        'default_cooldown': 0,
        'has_rules': True,
        'rules_type': 'gift' },
    'sc': {
        'label': '醒目留言 (SC)',
        'icon': 'star',
        'default_enabled': True,
        'default_strength': 80,
        'default_pulse': 'CS2-受伤',
        'default_action': 'both',
        'default_duration': 2,
        'default_cooldown': 5,
        'has_rules': False },
    'guard': {
        'label': '上舰/续费舰长',
        'icon': 'anchor',
        'default_enabled': True,
        'default_strength': 100,
        'default_pulse': 'CS2-死亡',
        'default_action': 'both',
        'default_duration': 3,
        'default_cooldown': 10,
        'has_rules': False } }
GUARD_LEVEL_NAMES = {
    1: '总督',
    2: '提督',
    3: '舰长' }
