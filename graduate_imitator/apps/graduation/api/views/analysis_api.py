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
from pydub import AudioSegment
import numpy as np
import json
from graduate_imitator.apps.graduation.domain.repositories.question_repository import *
from graduate_imitator.apps.graduation.domain.services.speech_to_text_service import *

audio_parser = SpeechToTextService()

class AnalyzeUserAnswers(APIView):
    def post(self, request):
        # todo: не работает расшифровка текста нормально (speech_to_text_service.py), тут написано только вычленение слов, нужно дописать вычленение ключевых и подсчёт процента использования ключевых
        responses = []
        # Перебираем все загруженные файлы
        for key in request.FILES:
            file = request.FILES[key]

            # Используем pydub для чтения аудиофайла
            audio_segment = AudioSegment.from_file(file)

            # Ensure the audio is mono
            if audio_segment.channels > 1:
                audio_segment = audio_segment.set_channels(1)

            # Resample to 16kHz as Whisper expects this for direct array input
            WHISPER_SAMPLE_RATE = 16000
            if audio_segment.frame_rate != WHISPER_SAMPLE_RATE:
                audio_segment = audio_segment.set_frame_rate(WHISPER_SAMPLE_RATE)

            # Ensure 16-bit sample width for consistent normalization
            # Whisper's reference normalization is for 16-bit audio ( / 32768.0)
            if audio_segment.sample_width != 2:  # 2 bytes = 16 bits
                audio_segment = audio_segment.set_sample_width(2)

            # Convert to float32 numpy array
            samples = np.array(audio_segment.get_array_of_samples()).astype(np.float32)
            # Normalize to [-1.0, 1.0] for 16-bit audio
            samples /= 32768.0

            # Transcribe audio (sample_rate parameter is removed from transcribe_audio)
            text = audio_parser.transcribe_audio(samples, language="ru")
            responses.append({"file": key, "text": text})

        # response_delays = []
        # response_durations = []
        # length = request.POST.get("length")
        # try:
        #     length = int(length)
        # except Exception as e:
        #     return Response(
        #         {"error": f"Не удалось int(length): {e}"}
        #     )
        #
        # for i in range(length):
        #     # question_id = request.POST.get("answers[${index}][question_id]")
        #     responseDelay = request.POST.get(f"answers[{i}][responseDelay]")
        #     responseDuration = request.POST.get(f"answers[{i}][responseDuration]")
        #     try:
        #         responseDelay = float(responseDelay) if responseDelay and responseDelay != "null" else 0
        #         responseDuration = float(responseDuration) if responseDuration and responseDuration != "null" else 0
        #     except Exception as e:
        #         return Response(
        #             {"error": f"Не удалось float(штука): {e}, {responseDelay}, {responseDuration}"}
        #         )
        #     responseDelay = min(responseDelay / 5, 1)
        #     responseDuration = min(responseDuration / 15, 1)
        #     response_delays.append(responseDelay)
        #     response_durations.append(responseDuration)
        #
        # delay_percentage = sum(response_delays) / len(response_delays) * 100
        # duration_percentage = sum(response_durations) / len(response_durations) * 100

        return Response(
            {"debug": responses,
             "keywords_percentage": 0,
             "delay_percentage": 11,
             "duration_percentage": 1},
            status=status.HTTP_200_OK
        )

    def get(self, request):
        return Response(
            {'message': 'Эндпоинт аналитики работает'},
            status=status.HTTP_200_OK
        )
