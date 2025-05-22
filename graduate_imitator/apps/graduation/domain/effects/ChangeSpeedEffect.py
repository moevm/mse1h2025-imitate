from torchaudio.functional import resample
from .abstract.EffectBase import EffectBase
from .abstract.AudioEffect import AudioEffect


class ChangeSpeedEffect(EffectBase, AudioEffect):
    name = 'Скорость речи'
    description = 'Меняет скорость речи'
    input_tag = '<input type="range" name="effects" min="0.5" max="1.5" step="0.1" value="1.0">'

    def apply(self, audio, sample_rate: int, speed_factor: float = 1.0):
        return resample(
            audio,
            orig_freq=int(sample_rate * speed_factor),
            new_freq=sample_rate
        )