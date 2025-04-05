# import pytest
# from mse1h2025_imitate.graduation_imitator.models.question import Question
# from mse1h2025_imitate.graduation_imitator.repositories.question_repository import QuestionRepository
#
#
# @pytest.mark.django_db
# def test_get_questions_by_keywords_any():
#
#     q1 = Question.objects.create(
#         question_text="Что такое Django?",
#         category="web",
#         difficulty_level=1,
#         keywords=["django", "python"]
#     )
#     q2 = Question.objects.create(
#         question_text="Что такое SQL?",
#         category="db",
#         difficulty_level=2,
#         keywords=["sql", "database"]
#     )
#     q3 = Question.objects.create(
#         question_text="Как работает кэш?",
#         category="graduation_imitator",
#         difficulty_level=2,
#         keywords=["cache", "redis"]
#     )
#
#     result = QuestionRepository.get_questions_by_keywords_any(["django", "redis"])
#     result_ids = {q.id for q in result}
#     assert q1.id in result_ids
#     assert q3.id in result_ids
#     assert q2.id not in result_ids
#
#
# @pytest.mark.django_db
# def test_get_questions_by_keywords_all():
#     q1 = Question.objects.create(
#         question_text="Комбинированный вопрос",
#         category="mix",
#         difficulty_level=3,
#         keywords=["django", "python", "sql"]
#     )
#     q2 = Question.objects.create(
#         question_text="Только про Django",
#         category="web",
#         difficulty_level=1,
#         keywords=["django"]
#     )
#
#     result = QuestionRepository.get_questions_by_keywords_all(["django", "python"])
#
#     result_ids = {q.id for q in result}
#     assert q1.id in result_ids
#     assert q2.id not in result_ids
