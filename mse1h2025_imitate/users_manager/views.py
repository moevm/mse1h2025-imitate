from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views import View
from rest_framework import status
from django.contrib.auth import authenticate, login
from users_manager.serializers import UserSerializer, UserLoginSerializer
from django.core.exceptions import PermissionDenied
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from pathlib import Path
from os.path import join as path_join
from django.shortcuts import render, redirect
from json import loads, JSONDecodeError
from json import dumps as json_dumps

TEMPLATES_DIR = path_join(Path(__file__).resolve().parent.parent, "templates", "users_manager")


class MyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Hello, world!"})


class RegisterFrontView(View):
    def get(self, request):
        # Получаем контекст из GET-параметров
        context = {}
        if 'context_for_front' in request.GET:
            try:
                # Декодируем JSON-строку в словарь
                context = loads(request.GET['context_for_front'])
            except JSONDecodeError:
                context = {}  # Если не удалось декодировать, используем пустой контекст
        return render(request, path_join(TEMPLATES_DIR, "register.html"), context)


class LoginFrontView(View):
    def get(self, request):
        # Получаем контекст из GET-параметров
        context = {}
        if 'context_for_front' in request.GET:
            try:
                # Декодируем JSON-строку в словарь
                context = loads(request.GET['context_for_front'])
            except JSONDecodeError:
                context = {}  # Если не удалось декодировать, используем пустой контекст
        return render(request, path_join(TEMPLATES_DIR, "login.html"), context)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            try:
                error_message = str(errors[list(errors.keys())[0]][0])
                return Response(
                    {'error': error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {'error': str(errors)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            user = serializer.save()
            login(request, user)
            return Response(
                {'message': 'User registered and logged in successfully'},
                status=status.HTTP_201_CREATED
            )
        except IntegrityError as e:
            return Response(
                {'error': 'User registration failed', 'details': 'Username already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Failed to register user', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )

            if not user:
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            active_sessions = Session.objects.filter(
                expire_date__gte=timezone.now(),
                session_data__contains=f'"auth_user_id":{user.id}'
            )

            if active_sessions.exists():
                active_sessions.delete()

            login(request, user)

            if not request.session.session_key:
                return Response(
                    {'error': 'Session cookie not set'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                {'message': 'Login successful', 'sessionid': request.session.session_key},
                status=status.HTTP_200_OK
            )

        except ObjectDoesNotExist as e:
            return Response(
                {'error': 'Session error', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            return Response(
                {'error': 'Login failed', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(View):
    def get(self, request):
        return self._handle_logout(request)

    def _handle_logout(self, request):
        try:
            if not request.user.is_authenticated:
                raise PermissionDenied("User is not authenticated.")

            if 'sessionid' not in request.COOKIES:
                raise PermissionDenied("Session ID is missing in cookies.")

            session_key = request.COOKIES['sessionid']
            try:
                session = Session.objects.get(session_key=session_key)
            except Session.DoesNotExist:
                raise PermissionDenied("Session does not exist.")

            logout(request)

            session.delete()

            response = JsonResponse({"message": "Successfully logged out."}, status=200)
            response.delete_cookie('sessionid')
            return response

        except PermissionDenied as e:
            return JsonResponse({"error": str(e)}, status=403)

        except Exception as e:
            return JsonResponse({"error": "An error occurred during logout."}, status=500)


class ProfileView(View):
    def get(self, request):
        return render(request, path_join(TEMPLATES_DIR, "profile.html"))
