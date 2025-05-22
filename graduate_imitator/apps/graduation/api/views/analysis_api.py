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
from graduate_imitator.apps.graduation.domain.repositories.question_repository import *
from graduate_imitator.apps.graduation.domain.services.text_to_speach_service import *


class AnalyzeUserAnswers(APIView):

    def post(self, request):
        pass

    def get(self, request):
        return Response(
            {'message': 'Эндпоинт работает'},
            status=status.HTTP_200_OK
        )
