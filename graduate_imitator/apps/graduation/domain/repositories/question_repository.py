from django.db.models import Q
from ..models.question import Question
from functools import reduce
from operator import and_


class QuestionRepository:
    @staticmethod
    def get_questions_by_keywords_any(keywords):
        if not keywords:
            return Question.objects.none()  # Возвращаем пустой QuerySet, если нет ключевых слов
        query = Q()
        for kw in keywords:
            query |= Q(keywords__contains=kw)  # Убираем квадратные скобки
        return Question.objects.filter(query)

    @staticmethod
    def get_questions_by_keywords_all(keywords):
        if not keywords:
            return Question.objects.none()  # Возвращаем пустой QuerySet, если нет ключевых слов
        query = reduce(and_, (Q(keywords__contains=kw) for kw in keywords))  # через reduce и убрали квадратные скобки
        return Question.objects.filter(query)

    @staticmethod
    def get_answer_keywords_by_id(question_id):
        try:
            question = Question.objects.get(id=question_id)
            return question.answer_keywords
        except Question.DoesNotExist:
            return []  # Возвращаем None, если вопрос с таким ID не найден
