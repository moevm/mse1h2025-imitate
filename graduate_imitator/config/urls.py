from graduate_imitator.apps.graduation.api.views.users import RegisterAPIView, LoginAPIView, LogoutAPIView
from graduate_imitator.apps.graduation.interfaces.web.views import RegisterWebView, LoginWebView
from graduate_imitator.apps.graduation.api.views.presentation import load_presentation
from django.contrib import admin
from django.urls import path, include
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
    # API Endpoints
    path('api/users/register', RegisterAPIView.as_view(), name='api-register'),
    path('api/users/login', LoginAPIView.as_view(), name='api-login'),
    path('api/users/logout', LogoutAPIView.as_view(), name='api-logout'),
    path('api/presentation/load', load_presentation),
    
    # Web Views
    path('register', RegisterWebView.as_view(), name='web-register'),
    path('login', LoginWebView.as_view(), name='web-login'),
    
    #Swagger
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin', admin.site.urls),

    #CSRF
    path('api/csrf_token/', get_csrf_token, name='csrf_token'),
]