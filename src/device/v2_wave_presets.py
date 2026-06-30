# Source Generated with Decompyle++
# File: v2_wave_presets.pyc (Python 3.11)

'''郊狼 2.0 波形预设库 — (X, Y, Z) 三参数格式

V2 BLE 协议每个通道用 20 bits 打包到 3 字节，超出范围会触发
``int too big to convert`` 异常：

X (0-31, 5 bits):   连续脉冲数，每脉冲 1ms
Y (0-1023, 10 bits): 脉冲后暂停周期数，每周期 1ms
Z (0-31, 5 bits):    脉冲宽度（值越大体感越强）
'''
V2_WAVE_PRESETS = {
    'CS2-受伤': {
        'description': '渐强冲击（V2 简化）',
        'wave_x': 5,
        'wave_y': 15,
        'wave_z': 20 },
    'CS2-闪光': {
        'description': '持续高强度（V2 简化）',
        'wave_x': 10,
        'wave_y': 5,
        'wave_z': 28 },
    'CS2-烟雾': {
        'description': '中等强度脉冲（V2 简化）',
        'wave_x': 5,
        'wave_y': 20,
        'wave_z': 15 },
    'CS2-燃烧': {
        'description': '波动灼烧感（V2 简化）',
        'wave_x': 8,
        'wave_y': 10,
        'wave_z': 22 },
    'CS2-死亡': {
        'description': '长时间满强度（V2 简化）',
        'wave_x': 15,
        'wave_y': 3,
        'wave_z': 31 },
    '呼吸': {
        'description': '缓慢节奏，模拟呼吸',
        'wave_x': 3,
        'wave_y': 30,
        'wave_z': 15 },
    '潮汐': {
        'description': '平缓起伏',
        'wave_x': 5,
        'wave_y': 20,
        'wave_z': 18 },
    '连击': {
        'description': '快速连续冲击',
        'wave_x': 10,
        'wave_y': 5,
        'wave_z': 25 },
    '快速按捏': {
        'description': '极短一击',
        'wave_x': 2,
        'wave_y': 25,
        'wave_z': 28 },
    '心跳节奏': {
        'description': '双脉冲心跳节奏',
        'wave_x': 8,
        'wave_y': 15,
        'wave_z': 24 },
    '颗粒摩擦': {
        'description': '短促持续',
        'wave_x': 12,
        'wave_y': 3,
        'wave_z': 22 },
    '波浪涟漪': {
        'description': '快速起伏',
        'wave_x': 5,
        'wave_y': 10,
        'wave_z': 20 } }

def v3_waveform_to_v2(waveform = None):
    '''将 V3 帧格式波形近似转换为 V2 (X, Y, Z) 参数

    V2 BLE 协议 (Z<<15 | Y<<5 | X) 必须打包到 3 字节 = 24 bits：
      - X: 0-31  (5 bits)
      - Y: 0-1023 (10 bits)
      - Z: 0-31  (实际只能 5 bits，超过 31 时 Z<<15 会爆 24 bits)

    取全帧的平均频率和最大强度（而非仅第一帧），避免 ramp-up 波形
    （如 CS2-受伤 首帧强度=0）算出 Z=0 导致设备不电击。
    '''
    if not waveform:
        return (5, 15, 20)
    all_freqs = None
    all_strengths = []
    for frame in waveform:
        all_freqs.extend(frame[0])
        all_strengths.extend(frame[1])
    avg_freq = sum(all_freqs) / len(all_freqs) if all_freqs else 10
    max_strength = max(all_strengths) if all_strengths else 50
    x = max(1, min(31, int(avg_freq)))
    z = max(1, min(31, int(max_strength * 31 / 100)))
    y = max(1, min(1023, int((100 - max_strength) * 5 + 5)))
    return (x, y, z)

