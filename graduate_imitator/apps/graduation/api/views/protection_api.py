from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
    OpenApiExample,
    OpenApiResponse
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from graduate_imitator.apps.graduation.domain.repositories.question_repository import QuestionRepository

class StartProtectionAPIView(APIView):
    @extend_schema(
        summary="Начать защиту",
        description=(
                "Запускает процедуру защиты: по списку ключевых слов возвращает "
                "массив вопросов, которые будут использоваться во время защиты."
        ),
        parameters=[
            OpenApiParameter(
                name="keywords",
                description="Список ключевых слов через запятую (например: math,physics,algebra)",
                required=True,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                examples=[
                    OpenApiExample(name="single", value="calculus"),
                    OpenApiExample(name="multiple", value="calculus,algebra,geometry"),
                ],
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Защита успешно запущена, возвращён список вопросов",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="success",
                        value={
                            "message": "Защита началась",
                            "questions": [
                                {"id": 1, "text": "Что такое предел функции?"},
                                {"id": 5, "text": "Дайте определение группы в алгебре."},
                            ],
                        },
                    ),
                ],
            ),
            500: OpenApiResponse(
                description="Внутренняя ошибка сервера",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(name="error", value={"error": "описание ошибки"}),
                ],
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        try:
            raw = request.query_params.get("keywords", "")
            keywords = [kw.strip() for kw in raw.split(",") if kw.strip()]
            questions = QuestionRepository.get_questions_by_keywords_any(keywords)
            return Response(
                {"message": "Защита началась", "questions": list(questions)},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
