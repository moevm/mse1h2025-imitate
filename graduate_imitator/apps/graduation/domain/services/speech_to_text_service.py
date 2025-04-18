import whisper
import torch


class SpeechToTextService:

    def __init__(self, model_name: str = "base"):
        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model = whisper.load_model(model_name).to(self.device)
        except Exception as e:
            raise Exception(f"Error loading Whisper model: {e}")

    def transcribe_audio(self, audio_path: str, language: str = None) -> str:
        try:
            transcription = self.model.transcribe(audio_path, language=language)
            return transcription["text"]
        except Exception as e:
            raise Exception(f"Error during speech-to-text transcription: {e}")
    