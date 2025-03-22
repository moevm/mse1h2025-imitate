import torch
import soundfile as sf

class TextToSpeechService:

    def __init__(self):
        self.language = 'ru'
        self.model_id = 'v4_ru'
        self.sample_rate = 48000
        self.speaker = 'xenia'
        self.device = torch.device('cpu')

    def get_speech_by_text(self, text):
        model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                             model='silero_tts',
                                             language=self.language,
                                             speaker=self.model_id)
        model.to(self.device)

        audio = model.apply_tts(text=text,
                                speaker=self.speaker,
                                sample_rate=self.sample_rate)
        return audio

