from django.views import View
from django.shortcuts import render
from os.path import join as path_join
from django.shortcuts import render, redirect
from json import loads, JSONDecodeError
from json import dumps as json_dumps
from pathlib import Path
import json

from graduate_imitator.apps.graduation.domain.effects.abstract.EffectBase import EffectBase
from graduate_imitator.apps.graduation.domain.effects import *

class RegisterWebView(View):
    def get(self, request):
        context = {}
        if 'context_for_front' in request.GET:
            try:
                context = loads(request.GET['context_for_front'])
            except JSONDecodeError:
                context = {}
        return render(request, "user/register.html", context)


class LoginWebView(View):
    def get(self, request):
        context = {}
        if 'context_for_front' in request.GET:
            try:
                context = loads(request.GET['context_for_front'])
            except JSONDecodeError:
                context = {}  # Если не удалось декодировать, используем пустой контекст
        return render(request, "user/login.html", context)


class ProfileWebView(View):
    def get(self, request):
        context = {}
        if 'context_for_front' in request.GET:
            try:
                context = loads(request.GET['context_for_front'])
            except JSONDecodeError:
                context = {}
        return render(request, "user/profile.html", context)


"""
пример создания данных для отображения на странице профиля:


from ...domain.repositories.user_repository import UserRepository
from ...domain.repositories.presentation_repository import PresentationRepository
from ...domain.repositories.attempt_repository import AttemptRepository
from datetime import datetime
from random import randint

user = UserRepository.get_user_by_id(request.user.id)
PresentationRepository.create_presentation(user, "Title yo", "Filepath yo")
now1 = datetime.now()
now2 = datetime.now()
presentation = PresentationRepository.get_presentations_by_user_id(user)[0]
AttemptRepository.create_attempt(user, presentation, now1, now2, randint(0, 100), True)

# получение защит 
user = UserRepository.get_user_by_id(request.user.id)
results = AttemptRepository.get_attempts_by_user_id(user)
if len(results) > 10:
    for r in results:
        AttemptRepository.delete_attempt(r.id)
"""


class HomeWebView(View):
    def get(self, request):
        context = {}
        if 'context_for_front' in request.GET:
            try:
                context = loads(request.GET['context_for_front'])
            except JSONDecodeError:
                context = {}
        return render(request, "home/home.html", context)
    

class ProtectionWebView(View):
    def get(self, request):
        context = {}
        if 'context_for_front' in request.GET:
            try:
                context = loads(request.GET['context_for_front'])
            except JSONDecodeError:
                context = {}
        return render(request, "protection/protection.html", context)
    

class AnswerWebView(View):
    def get(self, request):
        return redirect("web-protection")  # если напрямую зашёл

    def post(self, request):
        context = {}
        print(f"[AnswerWebView] Received POST data: {request.POST}")
        try:
            questions = loads(request.POST.get("questions", "[]"))
            speaker_info = loads(request.POST.get("speakerInfo", "{}"))
            presentation_id = request.POST.get("presentation_id")
            print(f"[AnswerWebView] Extracted presentation_id: {presentation_id}")
        except JSONDecodeError:
            questions = []
            speaker_info = {}
            presentation_id = None
        except Exception as e:
            print(f"Error retrieving POST data in AnswerWebView: {e}")
            questions = []
            speaker_info = {}
            presentation_id = None

        print(EffectBase.__subclasses__())

        context = {
                'questions': questions,
                'speakerInfo': speaker_info,
                'effects': EffectBase.__subclasses__(),
                'presentation_id': presentation_id,
        }

        if presentation_id is None:
            print("Warning: presentation_id was not found in POST request to AnswerWebView")

        return render(request, "protection/answer.html", context)


class ResultsWebView(View):
    # def get(self, request):
    #     return redirect("web-protection")  # если напрямую зашёл

    def get(self, request):
        results = request.session.get("results", {})
        return render(request, "protection/results.html", {'results': results})
