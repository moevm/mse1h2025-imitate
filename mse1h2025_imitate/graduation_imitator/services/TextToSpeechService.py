import torch


class TextToSpeechService:

    def __init__(self, language: str, model_id: str, speaker: str):
        self.sample_rate = 48000
        self.speaker = speaker
        self.device = torch.device('cpu')
        try:
            self.model, _ = torch.hub.load(
                repo_or_dir='snakers4/silero-models',
                model='silero_tts',
                language=language,
                speaker=model_id,
                trust_repo=True
            )
        except Exception as e:
            raise Exception(f"Error loading TTS model: {e}")

    def get_speech_by_text(self, text):
        try:
            self.model.to(self.device)
        except Exception as e:
            raise Exception(f"Error moving model to device {self.device}: {e}")

        try:
            audio = self.model.apply_tts(
                text=text,
                speaker=self.speaker,
                sample_rate=self.sample_rate
            )
        except Exception as e:
            raise Exception(f"Error during text-to-speech conversion: {e}")

        return audio
