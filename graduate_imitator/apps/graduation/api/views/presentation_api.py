from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from graduate_imitator.apps.graduation.infrastructure.utils.presentation_processing import PresentationProcessingService
from graduate_imitator.apps.graduation.domain.repositories.presentation_repository import PresentationRepository
from django.core.files.storage import default_storage
import os

@require_POST
def upload_presentation_and_extract_keywords(request):
    file = request.FILES.get('presentation')

    if not file:
        return JsonResponse({'error_msg': 'Файл не загружен'}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({'error_msg': 'Пользователь не аутентифицирован'}, status=401)

    user_id = request.user.id
    file_name = file.name
    title = os.path.splitext(file_name)[0]

    try:
        file_path_within_media_root = os.path.join('presentations', f'user_{user_id}', file_name)
        saved_file_path = default_storage.save(file_path_within_media_root, file)
        
        presentation = PresentationRepository.create_presentation(
            user_id=user_id,
            title=title,
            file_path=saved_file_path
        )
        print(f"[PresentationAPI] Created presentation object: {presentation}")
        if presentation:
            print(f"[PresentationAPI] Created presentation with ID: {presentation.id}, type: {type(presentation.id)}")
        else:
            print("[PresentationAPI] Failed to create presentation object.")

        with default_storage.open(saved_file_path, 'rb') as saved_file_for_keywords:
            keywords = PresentationProcessingService.get_10_keywords(saved_file_for_keywords)
        
        current_presentation_id = None
        if presentation and hasattr(presentation, 'id'):
            current_presentation_id = presentation.id

        return JsonResponse({'keywords': keywords, 'presentation_id': current_presentation_id}, status=200)
    
    except Exception as e:
        return JsonResponse({'error_msg': f'Ошибка при обработке файла: {str(e)}'}, status=500)