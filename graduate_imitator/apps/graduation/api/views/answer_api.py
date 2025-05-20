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

class TextToSpeechAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            text = data.get('text')
            speaker = data.get('speaker')
            model_id = data.get('model_id')
            language = data.get('language')

            if not all([text, speaker, model_id, language]):
                return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

            tts = TextToSpeechService(language='ru', model_id='v4_ru', speaker=speaker)
            question_tts = {
                    'name': speaker,
                    'model_id': 'v4_ru',
                    'language': 'ru',
                    'audio_sample': convert_tensor_to_base64(
                        tts.get_speech_by_text(text),
                        tts.sample_rate
                    )
                }
        except Exception as e:
            return JsonResponse({'error': e}, status=400)
        return JsonResponse({'question_tts': question_tts}, status=200)