# Source Generated with Decompyle++
# File: events.pyc (Python 3.11)

'''Douyin live event definitions shared by backend and future UI.'''
FRAME_MS = 100
EVENT_DEFS = {
    'chat': {
        'label': 'Chat',
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
        'label': 'Gift',
        'icon': 'gift',
        'default_enabled': True,
        'default_strength': 30,
        'default_pulse': 'CS2-燃烧',
        'default_action': 'both',
        'default_duration': 1.5,
        'default_cooldown': 0,
        'has_rules': True,
        'rules_type': 'gift' },
    'like': {
        'label': 'Like',
        'icon': 'thumbs-up',
        'default_enabled': False,
        'default_strength': 10,
        'default_pulse': 'CS2-受伤',
        'default_action': 'waveform',
        'default_duration': 0.5,
        'default_cooldown': 5,
        'has_rules': False },
    'member': {
        'label': 'Entry',
        'icon': 'log-in',
        'default_enabled': False,
        'default_strength': 10,
        'default_pulse': 'CS2-受伤',
        'default_action': 'waveform',
        'default_duration': 0.5,
        'default_cooldown': 2,
        'has_rules': False },
    'follow': {
        'label': 'Follow',
        'icon': 'user-plus',
        'default_enabled': True,
        'default_strength': 20,
        'default_pulse': 'CS2-受伤',
        'default_action': 'both',
        'default_duration': 1,
        'default_cooldown': 2,
        'has_rules': False },
    'room_stats': {
        'label': 'Room stats',
        'icon': 'bar-chart-3',
        'default_enabled': False,
        'default_strength': 0,
        'default_pulse': 'CS2-受伤',
        'default_action': 'waveform',
        'default_duration': 0,
        'default_cooldown': 0,
        'has_rules': False } }
