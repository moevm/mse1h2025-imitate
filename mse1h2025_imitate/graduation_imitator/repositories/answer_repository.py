from django.core.exceptions import ObjectDoesNotExist
import logging
from ..models.answer import Answer

logger = logging.getLogger(__name__)


class AnswerRepository:
    @staticmethod
    def create_answer(attempt_id, question_id, user_answer, answered_at, accuracy_score, analysis_results):
        answer = Answer(
            attempt_id=attempt_id,
            question_id=question_id,
            user_answer=user_answer,
            answered_at=answered_at,
            accuracy_score=accuracy_score,
            analysis_results=analysis_results
        )
        answer.save()
        return answer

    @staticmethod
    def get_answer_by_id(answer_id):
        try:
            return Answer.objects.get(id=answer_id)
        except ObjectDoesNotExist:
            logger.warning(f"Answer with id {answer_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error retrieving answer by id: {e}")
            return None

    @staticmethod
    def get_answers_by_question_id(question_id):
        try:
            return Answer.objects.filter(question_id=question_id)
        except Exception as e:
            logger.error(f"Error retrieving answers for question_id {question_id}: {e}")
            return None

    @staticmethod
    def update_user_answer(answer_id, new_user_answer):
        try:
            answer = Answer.objects.get(id=answer_id)
            answer.user_answer = new_user_answer
            # todo обновление accuracy_score?
            # todo обновление analysis_results?
            answer.save()
            return answer
        except ObjectDoesNotExist:
            logger.warning(f"Answer with id {answer_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error updating user answer for id {answer_id}: {e}")
            return None

    @staticmethod
    def update_accuracy_score(answer_id, new_accuracy_score):
        try:
            answer = Answer.objects.get(id=answer_id)
            answer.accuracy_score = new_accuracy_score
            answer.save()
            return answer
        except ObjectDoesNotExist:
            logger.warning(f"Answer with id {answer_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error updating accuracy score for id {answer_id}: {e}")
            return None

    @staticmethod
    def update_analysis_results(answer_id, new_analysis_results):
        try:
            answer = Answer.objects.get(id=answer_id)
            answer.analysis_results = new_analysis_results
            answer.save()
            return answer
        except ObjectDoesNotExist:
            logger.warning(f"Answer with id {answer_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error updating analysis results for id {answer_id}: {e}")
            return None

    @staticmethod
    def delete_answer(answer_id):
        try:
            answer = Answer.objects.get(id=answer_id)
            answer.delete()
            return True
        except ObjectDoesNotExist:
            logger.warning(f"Answer with id {answer_id} does not exist.")
            return False
        except Exception as e:
            logger.error(f"Error deleting answer with id {answer_id}: {e}")
            return False

    @staticmethod
    def get_all_answers():
        try:
            return Answer.objects.all()
        except Exception as e:
            logger.error(f"Error retrieving all answers: {e}")
            return None
