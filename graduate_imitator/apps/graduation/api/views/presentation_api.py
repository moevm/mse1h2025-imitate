from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from graduate_imitator.apps.graduation.infrastructure.utils.presentation_processing import PresentationProcessingService

@require_POST
def upload_presentation_and_extract_keywords(request):
    file = request.FILES.get('presentation')

    if not file:
        return JsonResponse({'error_msg': 'Файл не загружен'}, status=400)

    keywords = PresentationProcessingService.get_10_keywords(file)
    return JsonResponse({'keywords': keywords}, status=200)