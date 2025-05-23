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
        # responses = []
        # # Перебираем все загруженные файлы
        # for key in request.FILES:
        #     file = request.FILES[key]
        #
        #     # Используем pydub для чтения аудиофайла
        #     audio_segment = AudioSegment.from_file(file)
        #     wav_file = io.BytesIO()
        #     audio_segment.export(wav_file, format="wav")
        #     wav_file.seek(0)
        #     # Преобразуем в numpy массив
        #     audio_data = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
        #
        #     # Если аудио стерео, преобразуем в моно, усредняя каналы
        #     if audio_segment.channels == 2:
        #         audio_data = audio_data.reshape((-1, 2)).mean(axis=1)
        #
        #     # Нормализуем аудиоданные в диапазоне [-1.0, 1.0]
        #     audio_data /= np.max(np.abs(audio_data))
        #
        #     # Транскрибируем аудио
        #     text = audio_parser.transcribe_audio(audio_data, "ru")
        #     responses.append({"file": key, "text": text})

        response_delays = []
        response_durations = []
        length = request.POST.get("length")
        try:
            length = int(length)
        except Exception as e:
            return Response(
                {"error": f"Не удалось int(length): {e}"}
            )

        for i in range(length):
            # question_id = request.POST.get("answers[${index}][question_id]")
            responseDelay = request.POST.get(f"answers[{i}][responseDelay]")
            responseDuration = request.POST.get(f"answers[{i}][responseDuration]")
            try:
                responseDelay = float(responseDelay) if responseDelay and responseDelay != "null" else 0
                responseDuration = float(responseDuration) if responseDuration and responseDuration != "null" else 0
            except Exception as e:
                return Response(
                    {"error": f"Не удалось float(штука): {e}, {responseDelay}, {responseDuration}"}
                )
            responseDelay = min(responseDelay / 5, 1)
            responseDuration = min(responseDuration / 15, 1)
            response_delays.append(responseDelay)
            response_durations.append(responseDuration)

        delay_percentage = sum(response_delays) / len(response_delays) * 100
        duration_percentage = sum(response_durations) / len(response_durations) * 100

        return Response(
            {"keywords_percentage": 0,
             "delay_percentage": delay_percentage,
             "duration_percentage": duration_percentage},
            status=status.HTTP_200_OK
        )

    def get(self, request):
        return Response(
            {'message': 'Эндпоинт аналитики работает'},
            status=status.HTTP_200_OK
        )
