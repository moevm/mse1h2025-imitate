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
from graduate_imitator.apps.graduation.domain.repositories.question_repository import *


class StartProtectionAPIView(APIView):
    def get(self, request):
        try:
            keywords = request.data.get('keywords')
            questions = QuestionRepository.get_questions_by_keywords_any(keywords)
            # Здесь должен быть запуск защиты - когда появится логика защиты, здесь ее используем.
            return Response({"message": "Защита началась", questions: list(questions)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
