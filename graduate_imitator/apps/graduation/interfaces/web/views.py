from django.views import View
from django.shortcuts import render
from os.path import join as path_join
from django.shortcuts import render, redirect
from json import loads, JSONDecodeError
from json import dumps as json_dumps
from pathlib import Path


class RegisterWebView(View):
    def get(self, request):
        context = {}
        if 'context_for_front' in request.GET:
            try:
                # Декодируем JSON-строку в словарь
                context = loads(request.GET['context_for_front'])
            except JSONDecodeError:
                context = {}  # Если не удалось декодировать, используем пустой контекст
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
