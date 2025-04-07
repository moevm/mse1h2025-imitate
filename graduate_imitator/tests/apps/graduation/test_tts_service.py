import pytest
import torch
from graduate_imitator.apps.graduation.domain.services.text_to_speach_service import TextToSpeechService

@pytest.fixture(scope='session')
def tts_service():
    return TextToSpeechService('ru', 'v4_ru', 'xenia')

@pytest.mark.django_tts_service
def test_tts_service_must_return_not_empty_tensor(tts_service):
    test_text = "Привет, как дела?"
    audio = tts_service.get_speech_by_text(test_text)
    assert isinstance(audio, torch.Tensor), "Ожидался Tensor от PyTorch"
    assert audio.numel() > 0, "Тензор пустой"

@pytest.mark.django_tts_service
def test_tts_service_must_raise_if_empty_text(tts_service):
    with pytest.raises(Exception):
        tts_service.get_speech_by_text("")

@pytest.mark.django_tts_service
def test_tts_service_must_fail_if_too_long_text(tts_service):
    with pytest.warns(UserWarning, match='Text string is longer than 1000 symbols'):
        long_text = "Привет. " * 1000
        with pytest.raises(Exception, match="too long"):
            tts_service.get_speech_by_text(long_text)

@pytest.mark.parametrize("text", [
    "Привет!",
    "Как дела?",
    "Сегодня хорошая погода",
    "Django — это ужасы"
])
def test_tts_service_must_return_not_empty_tensor_if_varius_phrases(tts_service, text):
    audio = tts_service.get_speech_by_text(text)
    assert audio.numel() > 0
