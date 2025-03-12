from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views import View
from rest_framework import status
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer, UserLoginSerializer

class MyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Hello, world!"})

class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                login(request, user)
                return Response(
                    {'message': 'User registered and logged in successfully'}, 
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'error': 'Failed to register user', 'details': str(e)}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data) 
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                login(request, user)
                return Response(
                    {'message': 'Login successful'}, 
                    status=status.HTTP_200_OK
                )
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(View):
    def post(self, request):
        logout(request)
        response = JsonResponse({"message": "Successfully logged out."})
        response.delete_cookie('sessionid')
        return response