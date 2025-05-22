from rest_framework import serializers
from graduate_imitator.apps.graduation.domain.models import Question  # поправь путь, если другой

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text']  