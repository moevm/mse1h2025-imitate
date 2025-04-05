"""mse1h2025_imitate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from graduation_imitator.views.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.middleware.csrf import get_token
from django.http import JsonResponse


schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourproject.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

urlpatterns = [
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin', admin.site.urls),

    path('api/csrf_token/', get_csrf_token, name='csrf_token'),



    path('api/users/register', RegisterView.as_view(), name='register'),
    path('api/users/login', LoginView.as_view(), name='login'),
    path('api/users/logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterFrontView.as_view(), name='register-front'),
    path('login', LoginFrontView.as_view(), name='login-front'),
    path('', HomeFrontView.as_view(), name='home'),
    path('api/start-protection', StartProtectionView.as_view(), name='start-protection'),
    path('api/get-results', GetResultsView.as_view(), name='get-results'),
    path('api/get_user_status', UserStatusView.as_view(), name='get-status')
]


