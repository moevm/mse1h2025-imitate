import pytest
import torch

from mse1h2025_imitate.backend.text_to_speach_service import TextToSpeechService


@pytest.mark.django_tts_service
def test_tts_service_generates_audio():
    tts = TextToSpeechService()
    test_text = "Привет, как дела?"

    audio = tts.get_speech_by_text(test_text)

    assert isinstance(audio, torch.Tensor), "Ожидался Tensor от PyTorch"
    assert audio.numel() > 0, "Тензор пустой"


@pytest.mark.django_tts_service
def test_tts_with_empty_text_should_raise():
    tts = TextToSpeechService()
    with pytest.raises(Exception):
        tts.get_speech_by_text("")


@pytest.mark.django_tts_service
def test_tts_with_long_text_should_fail():
    tts = TextToSpeechService()
    long_text = "Привет. " * 1000  # 7000+ символов

    with pytest.raises(Exception, match="too long"):
        tts.get_speech_by_text(long_text)


@pytest.mark.parametrize("text", [
    "Привет!",
    "Как дела?",
    "Сегодня хорошая погода",
    "Django — это ужасы"
])
def test_tts_various_phrases(text):
    tts = TextToSpeechService()
    audio = tts.get_speech_by_text(text)
    assert audio.numel() > 0

