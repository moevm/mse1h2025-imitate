from django.db.models import Q
from ..models.question import Question

class QuestionRepository:
    @staticmethod
    def get_questions_by_keywords_any(keywords):
        query = Q()
        for kw in keywords:
            query |= Q(keywords__contains=[kw])
        return Question.objects.filter(query)

    @staticmethod
    def get_questions_by_keywords_all(keywords):
        qs = Question.objects.all()
        for kw in keywords:
            qs = qs.filter(keywords__contains=[kw])
        return qs
