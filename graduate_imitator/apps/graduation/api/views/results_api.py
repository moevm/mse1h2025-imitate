from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
from json import dumps as json_dumps
from json import loads, JSONDecodeError
from os.path import join as path_join
from pathlib import Path
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from graduate_imitator.apps.graduation.domain.repositories.attempt_repository import *

logger = logging.getLogger(__name__)


class GetResultsAPIView(APIView):
    def get(self, request):
        from ...domain.repositories.user_repository import UserRepository
        from ...domain.repositories.presentation_repository import PresentationRepository
        from ...domain.repositories.answer_repository import AnswerRepository
        from datetime import datetime
        from random import randint

        user = UserRepository.get_user_by_id(request.user.id)
        PresentationRepository.create_presentation(user, "Title yo", "Filepath yo")
        now1 = datetime.now()
        now2 = datetime.now()
        presentation = PresentationRepository.get_presentations_by_user_id(user)[0]
        AttemptRepository.create_attempt(user, presentation, now1, now2, randint(0, 100), True)

        try:
            print(request.user.id)
            user_id = request.user.id
            limit_param = request.GET.get('limit', 10)
            limit = int(limit_param)

            attempts = AttemptRepository.get_limited_attempts_by_user_id(user_id, limit)

            results = []
            if attempts:
                for attempt in attempts:
                    date_field = attempt.start_time
                    formatted_date = date_field.strftime('%d %b %Y %H:%M')
                    results.append({
                        "date": formatted_date,
                        "score": attempt.score
                    })

            return Response({"results": results}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving results: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)