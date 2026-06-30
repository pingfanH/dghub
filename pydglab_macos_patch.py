from __future__ import annotations


def apply_patches() -> None:
    try:
        import asyncio
        import pydglab.service as service
    except Exception:
        return

    if getattr(service, "_dghub_macos_patched", False):
        return

    async def keep_wave(self) -> None:
        index_a = 0
        index_b = 0

        try:
            while True:
                await asyncio.sleep(0.1)

                waves_a = list(getattr(self, "channelA_wave_set", None) or [(0, 0, 0)])
                waves_b = list(getattr(self, "channelB_wave_set", None) or [(0, 0, 0)])

                wave_a = waves_a[index_a % len(waves_a)]
                wave_b = waves_b[index_b % len(waves_b)]
                index_a += 1
                index_b += 1

                self.coyote.ChannelA.waveX = wave_a[0]
                self.coyote.ChannelA.waveY = wave_a[1]
                self.coyote.ChannelA.waveZ = wave_a[2]
                self.coyote.ChannelB.waveX = wave_b[0]
                self.coyote.ChannelB.waveY = wave_b[1]
                self.coyote.ChannelB.waveZ = wave_b[2]

                await service.v2.set_wave_(self.client, self.coyote.ChannelA, self.characteristics)
                await service.v2.set_wave_(self.client, self.coyote.ChannelB, self.characteristics)
        except asyncio.CancelledError:
            raise

    async def retainer(self) -> None:
        index_a = 0
        index_b = 0

        try:
            while True:
                await asyncio.sleep(0.1)

                waves_a = list(getattr(self, "channelA_wave_set", None) or [(0, 0, 0)])
                waves_b = list(getattr(self, "channelB_wave_set", None) or [(0, 0, 0)])

                wave_a = self.waveset_converter(waves_a[index_a % len(waves_a)])
                wave_b = self.waveset_converter(waves_b[index_b % len(waves_b)])
                index_a += 1
                index_b += 1

                self.coyote.ChannelA.wave.insert(0, wave_a[0])
                self.coyote.ChannelA.wave.pop()
                self.coyote.ChannelA.waveStrenth.insert(0, wave_a[1])
                self.coyote.ChannelA.waveStrenth.pop()
                self.coyote.ChannelB.wave.insert(0, wave_b[0])
                self.coyote.ChannelB.wave.pop()
                self.coyote.ChannelB.waveStrenth.insert(0, wave_b[1])
                self.coyote.ChannelB.waveStrenth.pop()

                await service.v3.write_strenth_(self.client, self.coyote, self.characteristics)
        except asyncio.CancelledError:
            raise

    service.dglab._keep_wave = keep_wave
    service.dglab_v3._retainer = retainer
    service._dghub_macos_patched = True
