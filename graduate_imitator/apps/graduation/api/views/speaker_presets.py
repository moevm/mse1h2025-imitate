from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiTypes
import torch
import soundfile as sf
import base64
import io

from graduate_imitator.apps.graduation.domain.services.text_to_speach_service import TextToSpeechService


def convert_tensor_to_base64(audio_tensor: torch.Tensor, sample_rate: int) -> str:
    audio_tensor = audio_tensor.detach().cpu().numpy()
    buf = io.BytesIO()
    sf.write(buf, audio_tensor, sample_rate, format='WAV')
    wav_bytes = buf.getvalue()
    b64 = base64.b64encode(wav_bytes).decode('utf-8')
    return f"data:audio/wav;base64,{b64}"


@extend_schema(
    description="Speaker presets",
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    name='success',
                    value={
                        'presets': [
                            {
                                'name': 'Speaker name',
                                'model_id': 'tts model',
                                'language': 'lang',
                                'audio_sample': 'base64 audio string'
                            }
                        ]
                    },
                ),
            ],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    name='error',
                    value={
                        'error_msg': 'error description here'
                    },
                ),
            ],
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def speaker_presets(request):
    demo_phrase = 'Проверьте качество звучания и выберите подходящие настройки.'
    speakers = (
        'aidar',
        'baya',
        'kseniya',
        'xenia',
        'eugene'
    )
    presets = []
    try:
        for speaker in speakers:
            tts = TextToSpeechService(language='ru', model_id='v4_ru', speaker=speaker)
            presets.append(
                {
                    'name': speaker,
                    'model_id': 'v4_ru',
                    'language': 'ru',
                    'audio_sample': convert_tensor_to_base64(
                        tts.get_speech_by_text(demo_phrase),
                        tts.sample_rate
                    )
                }
            )
    except Exception as e:
        return JsonResponse({'error': e}, status=400)
    return JsonResponse({'presets': presets}, status=200)