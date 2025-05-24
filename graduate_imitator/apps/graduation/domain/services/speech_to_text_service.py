import whisper
import torch
import numpy as np


class SpeechToTextService:

    def __init__(self, model_name: str = "base"):
        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model = whisper.load_model(model_name).to(self.device)
        except Exception as e:
            raise Exception(f"Error loading Whisper model: {e}")

    def transcribe_audio(self, audio_data: np.ndarray, language: str = None) -> str:
        try:
            # Ensure audio_data is on the same device as the model
            # Whisper expects float32 numpy array, pre-processed to 16kHz mono
            transcription = self.model.transcribe(audio_data, language=language)
            return transcription["text"]
        except Exception as e:
            raise Exception(f"Error during speech-to-text transcription: {e}")
