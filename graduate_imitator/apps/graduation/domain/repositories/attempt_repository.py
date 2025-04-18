from django.core.exceptions import ObjectDoesNotExist
import logging
from ..models.attempt import Attempt

logger = logging.getLogger(__name__)


class AttemptRepository:
    @staticmethod
    def create_attempt(user_id, presentation_id, start_time, end_time, score, completed):
        attempt = Attempt(
            user_id=user_id,
            presentation_id=presentation_id,
            start_time=start_time,
            end_time=end_time,
            score=score,
            completed=completed
        )
        attempt.save()
        return attempt

    @staticmethod
    def get_attempt_by_id(attempt_id):
        try:
            return Attempt.objects.get(id=attempt_id)
        except ObjectDoesNotExist:
            logger.warning(f"Attempt with id {attempt_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error retrieving attempt by id: {e}")
            return None

    @staticmethod
    def get_attempts_by_user_id(user_id):
        try:
            return Attempt.objects.filter(user_id=user_id)
        except Exception as e:
            logger.error(f"Error retrieving attempts for user_id {user_id}: {e}")
            return None

    @staticmethod
    def update_attempt(attempt_id, new_score=None, new_completed=None):
        try:
            attempt = Attempt.objects.get(id=attempt_id)
            if new_score is not None:
                attempt.score = new_score
            if new_completed is not None:
                attempt.completed = new_completed
            attempt.save()
            return attempt
        except ObjectDoesNotExist:
            logger.warning(f"Attempt with id {attempt_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error updating attempt with id {attempt_id} with {new_score} new_score, {new_completed} new_completed: {e}")
            return None

    @staticmethod
    def delete_attempt(attempt_id):
        try:
            attempt = Attempt.objects.get(id=attempt_id)
            attempt.delete()
            return True
        except ObjectDoesNotExist:
            logger.warning(f"Attempt with id {attempt_id} does not exist.")
            return False
        except Exception as e:
            logger.error(f"Error deleting attempt with id {attempt_id}: {e}")
            return False

    @staticmethod
    def get_all_attempts():
        try:
            return Attempt.objects.all()
        except Exception as e:
            logger.error(f"Error retrieving all attempts: {e}")
            return None

    @staticmethod
    def get_limited_attempts_by_user_id(user_id, limit):
        try:
            return list(Attempt.objects.filter(user_id=user_id).order_by('-start_time')[:limit])
        except Exception as e:
            logger.error(f"Error retrieving limited attempts for user_id {user_id} with limit {limit}: {e}")
            return None
