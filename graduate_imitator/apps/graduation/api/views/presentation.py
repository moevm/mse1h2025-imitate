# import io
# from django.http import JsonResponse
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.request import Request
# from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiTypes
# from graduate_imitator.apps.graduation.domain.dto.presentation_data import PresentationData
# from graduate_imitator.apps.graduation.infrastructure.utils.presentation_processing import PresentationProcessingService
# from zipfile import BadZipFile
#
#
# @extend_schema(
#     request={
#         'multipart/form-data': {
#             'type': 'object',
#             'properties': {
#                 'presentation': {
#                     'type': 'string',
#                     'format': 'binary',
#                 },
#             },
#             'required': ['presentation']
#         }
#     },
#     description="Presentation load",
#     responses={
#         200: PresentationData.model_json_schema(),
#         400: OpenApiResponse(
#             response=OpenApiTypes.OBJECT,
#             examples=[
#                 OpenApiExample(
#                     name='error',
#                     value={
#                         'error_msg': 'error description here'
#                     },
#                 ),
#             ],
#         )
#     }
# )
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def load_presentation(request: Request):
#     presentation_file = request.FILES.get('presentation')
#     if presentation_file is None:
#         return JsonResponse({'error_msg': 'There is no file in request'}, status=400)
#     file_data = io.BytesIO(
#         presentation_file.read()
#     )
#     try:
#         parsed_data = PresentationProcessingService.process_presentation(file_data)
#     except BadZipFile:
#         return JsonResponse({'error_msg': 'Bad filetype'}, status=400)
#     return JsonResponse(parsed_data.model_dump())
