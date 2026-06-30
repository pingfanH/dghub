# Source Generated with Decompyle++
# File: audio_kit.pyc (Python 3.11)

'''音频设备枚举与测试（sounddevice 封装）。'''
BASE_GAIN = 300

def list_input_devices():
    import sounddevice as sd
    devices = sd.query_devices()
    return enumerate(devices)()


def record_peak_percent(device_name = None, sensitivity = None):
    '''录制约 1 秒，返回 RMS / 峰值百分比（与实时监控同口径，受灵敏系数影响）。'''
    import numpy as np
    import sounddevice as sd
    device_id = None
# WARNING: Decompyle incomplete

