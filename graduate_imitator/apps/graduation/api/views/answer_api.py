# answer_api.py
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from graduate_imitator.apps.graduation.domain.services.text_to_speach_service import TextToSpeechService
import io
import soundfile as sf
import json
from graduate_imitator.apps.graduation.api.views.speaker_presets import convert_tensor_to_base64
from graduate_imitator.apps.graduation.domain.effects.abstract.EffectBase import EffectBase
from graduate_imitator.apps.graduation.domain.effects.abstract.TextEffect import TextEffect
from graduate_imitator.apps.graduation.domain.effects.abstract.AudioEffect import AudioEffect
from graduate_imitator.apps.graduation.domain.effects import *

class TextToSpeechAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            text = data.get('text')
            speaker = data.get('speaker')
            model_id = data.get('model_id')
            language = data.get('language')
            effects_values = data.get('effects')

            if not all([text, speaker, model_id, language]):
                return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

            tts = TextToSpeechService(language='ru', model_id='v4_ru', speaker=speaker)
            effect_classes = EffectBase.__subclasses__()
            for i, effect_class in enumerate(effect_classes):
                if issubclass(effect_class, TextEffect) and effects_values[i]:
                    text = effect_class().apply(text)

            audio = tts.get_speech_by_text(text)
            for i, effect_class in enumerate(effect_classes):
                if issubclass(effect_class, AudioEffect) and effects_values[i]:
                    if effect_class == ChangeSpeedEffect:
                        audio = effect_class().apply(audio, tts.sample_rate, effects_values[i])
                    else:
                        audio = effect_class().apply(audio, tts.sample_rate)

            question_tts = {
                    'name': speaker,
                    'model_id': 'v4_ru',
                    'language': 'ru',
                    'audio_sample': convert_tensor_to_base64(
                        audio,
                        tts.sample_rate
                    )
                }
        except Exception as e:
            return JsonResponse({'error': e}, status=400)
        return JsonResponse({'question_tts': question_tts}, status=200)