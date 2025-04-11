import os
import pytest
from graduate_imitator.apps.graduation.domain.services.speech_to_text_service import SpeechToTextService
from graduate_imitator.config.settings import BASE_DIR

@pytest.fixture(scope="session")
def stt_service():
    return SpeechToTextService(model_name="base")

@pytest.mark.django_stt_service
def test_stt_service_must_return_non_empty_string(stt_service):
    test_audio_path = os.path.join(BASE_DIR, "tests", "resources", "test_stt_service", "normal_speech.mp3")
    text = stt_service.transcribe_audio(test_audio_path, language="ru")
    assert isinstance(text, str), "Ожидалась строка"
    assert len(text.strip()) > 0, "Распознанный текст пустой"
    assert text.strip() == "Тест распознавания речи. Проверка.", "Текст распознан неверно"

@pytest.mark.django_stt_service
def test_stt_service_must_fail_if_file_does_not_exist(stt_service):
    test_audio_path = os.path.join(BASE_DIR, "tests", "resources", "test_stt_service", "does_not_exist.mp3")
    with pytest.raises(Exception, match="No such file or directory"):
        stt_service.transcribe_audio(test_audio_path, language="ru")

@pytest.mark.django_stt_service
def test_stt_service_must_raise_if_not_audio_file(stt_service, tmp_path):
    test_audio_path = os.path.join(BASE_DIR, "tests", "resources", "test_stt_service", "normal_speech.txt")
    with pytest.raises(Exception, match="Error during speech-to-text transcription"):
        stt_service.transcribe_audio(test_audio_path, language="ru")

@pytest.mark.parametrize("audio_file", [
    os.path.join(BASE_DIR, "tests", "resources", "test_stt_service", "normal_speech.aac"),
    os.path.join(BASE_DIR, "tests", "resources", "test_stt_service", "normal_speech.m4a"),
    os.path.join(BASE_DIR, "tests", "resources", "test_stt_service", "normal_speech.ogg"),
    os.path.join(BASE_DIR, "tests", "resources", "test_stt_service", "normal_speech.wav")
])
def test_stt_service_various_audio_formats(stt_service, audio_file):
    text = stt_service.transcribe_audio(audio_file, language="ru")
    assert len(text.strip()) > 0
