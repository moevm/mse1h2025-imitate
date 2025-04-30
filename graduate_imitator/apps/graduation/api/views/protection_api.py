from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
from json import dumps as json_dumps
from json import loads, JSONDecodeError
from os.path import join as path_join
from pathlib import Path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import io
import base64
import soundfile as sf
from rest_framework.permissions import AllowAny    # ← добавили сюда
from graduate_imitator.apps.graduation.domain.repositories.question_repository import *
from graduate_imitator.apps.graduation.domain.services.text_to_speach_service import *


class StartProtectionAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        for field in ('language', 'model_id', 'speaker'):
            if field not in request.data:
                return Response(
                    {"error": f"Missing field '{field}'"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        keywords = request.data.get('keywords', [])
        language = request.data['language']
        model_id = request.data['model_id']
        speaker = request.data['speaker']

        questions = QuestionRepository.get_questions_by_keywords_any(keywords)
        tts = TextToSpeechService(language, model_id, speaker)

        items = []
        for q in questions:
            audio_array = tts.get_speech_by_text(q.question_text)

            if isinstance(audio_array, torch.Tensor):
                audio_array = audio_array.detach().cpu().numpy()

            buf = io.BytesIO()
            sf.write(buf, audio_array, tts.sample_rate, format='WAV')
            wav_bytes = buf.getvalue()

            b64 = base64.b64encode(wav_bytes).decode('utf-8')
            items.append({
                "id": q.id,
                "text": q.question_text,
                "audio": f"data:audio/wav;base64,{b64}"
            })

        return Response(
            {"message": "Защита началась", "questions": items},
            status=status.HTTP_200_OK
        )