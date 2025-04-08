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
        try:
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