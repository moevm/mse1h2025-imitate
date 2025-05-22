import torch
import numpy as np
from .abstract.EffectBase import EffectBase
from .abstract.AudioEffect import AudioEffect


class EchoEffect(EffectBase, AudioEffect):
    name = 'Эхо'
    description = 'Добавляет эффект эхо'
    input_tag = '<input type="checkbox">'

    def apply(self, audio, sample_rate: int, delay_ms: int = 200, decay: float = 0.5):
        if audio.dim() == 1:
            audio = audio.unsqueeze(0)
        audio_np = audio.squeeze(0).numpy()
        delay_samples = int(delay_ms * sample_rate / 1000)
        echo_signal = np.zeros_like(audio_np)
        echo_signal[delay_samples:] = audio_np[:-delay_samples] * decay
        output = audio_np + echo_signal
        output = output / np.max(np.abs(output))
        return torch.reshape(torch.from_numpy(output).unsqueeze(0).to(audio.dtype).to(audio.device), (-1,))