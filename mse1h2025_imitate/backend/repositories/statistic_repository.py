from django.core.exceptions import ObjectDoesNotExist
import logging
from ..models.statistic import Statistic

logger = logging.getLogger(__name__)


class StatisticRepository:
    @staticmethod
    def create_statistic(user_id, total_attempts, avg_score, questions_answered, performance_data):
        statistic = Statistic(
            user_id=user_id,
            total_attempts=total_attempts,
            avg_score=avg_score,
            questions_answered=questions_answered,
            performance_data=performance_data
        )
        statistic.save()
        return statistic

    @staticmethod
    def get_statistic_by_user_id(user_id):
        try:
            return Statistic.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            logger.warning(f"Statistic for user_id {user_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error retrieving statistic by user_id: {e}")
            return None

    @staticmethod
    def update_total_attempts(user_id, num_attempts_to_add):
        try:
            statistic = Statistic.objects.get(user_id=user_id)
            statistic.total_attempts += num_attempts_to_add
            # todo обновление avg_score?
            # todo обновление performance_data?
            statistic.save()
            return statistic
        except ObjectDoesNotExist:
            logger.warning(f"Statistic for user_id {user_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error updating total attempts for user_id {user_id} adding {num_attempts_to_add} attempts: {e}")
            return None

    @staticmethod
    def update_avg_score(user_id, new_avg_score):
        # todo как вообще это работает?
        try:
            statistic = Statistic.objects.get(user_id=user_id)
            statistic.avg_score = new_avg_score
            # todo обновление performance_data?
            statistic.save()
            return statistic
        except ObjectDoesNotExist:
            logger.warning(f"Statistic for user_id {user_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error updating average score for user_id {user_id}: {e}")
            return None

    @staticmethod
    def update_questions_answered(user_id, num_questions_to_add):
        try:
            statistic = Statistic.objects.get(user_id=user_id)
            statistic.questions_answered = num_questions_to_add
            # todo обновление avg_score?
            # todo обновление performance_data?
            statistic.save()
            return statistic
        except ObjectDoesNotExist:
            logger.warning(f"Statistic for user_id {user_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error updating questions answered for user_id {user_id} adding {num_questions_to_add} questions: {e}")
            return None

    @staticmethod
    def update_all(user_id, total_attempts=None, avg_score=None, questions_answered=None):
        # todo как вообще это работает?
        try:
            statistic = Statistic.objects.get(user_id=user_id)
            if total_attempts is not None:
                statistic.total_attempts = total_attempts
            if avg_score is not None:
                statistic.avg_score = avg_score
            if questions_answered is not None:
                statistic.questions_answered = questions_answered
            statistic.save()
            return statistic
        except ObjectDoesNotExist:
            logger.warning(f"Statistic for user_id {user_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error updating statistic for user_id {user_id} with {total_attempts} attempts, {avg_score} avg_score, {questions_answered} questions: {e}")
            return None

    @staticmethod
    def delete_statistic(user_id):
        try:
            statistic = Statistic.objects.get(user_id=user_id)
            statistic.delete()
            return True
        except ObjectDoesNotExist:
            logger.warning(f"Statistic for user_id {user_id} does not exist.")
            return False
        except Exception as e:
            logger.error(f"Error deleting statistic for user_id {user_id}: {e}")
            return False

    @staticmethod
    def get_all_statistics():
        try:
            return Statistic.objects.all()
        except Exception as e:
            logger.error(f"Error retrieving all statistics: {e}")
            return None
