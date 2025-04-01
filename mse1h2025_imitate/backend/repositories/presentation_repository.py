from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import logging
from ..models.presentation import Presentation

logger = logging.getLogger(__name__)


class PresentationRepository:
    @staticmethod
    def create_presentation(user_id, title, file_path):
        presentation = Presentation(
            user_id=user_id,
            title=title,
            file_path=file_path
        )
        presentation.save()
        return presentation

    @staticmethod
    def get_presentations_by_user_id(user_id):
        try:
            return Presentation.objects.filter(user_id=user_id)
        except Exception as e:
            logger.error(f"Error retrieving presentations for user_id {user_id}: {e}")
            return None

    @staticmethod
    def get_presentation_by_id(presentation_id):
        try:
            return Presentation.objects.get(id=presentation_id)
        except ObjectDoesNotExist:
            logger.warning(f"Presentation with id {presentation_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error retrieving presentation by id: {e}")
            return None

    @staticmethod
    def update_presentation_title(presentation_id, new_title):
        try:
            presentation = Presentation.objects.get(id=presentation_id)
            presentation.title = new_title
            # todo: обновление file_path?
            presentation.save()
            return presentation
        except ObjectDoesNotExist:
            logger.warning(f"Presentation with id {presentation_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error updating presentation title for id {presentation_id}: {e}")
            return None

    @staticmethod
    def update_presentation_file_path(presentation_id, new_file_path):
        try:
            presentation = Presentation.objects.get(id=presentation_id)
            presentation.file_path = new_file_path
            # todo: обновление title?
            presentation.save()
            return presentation
        except ObjectDoesNotExist:
            logger.warning(f"Presentation with id {presentation_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error updating presentation file path for id {presentation_id}: {e}")
            return None

    @staticmethod
    def delete_presentation(presentation_id):
        try:
            presentation = Presentation.objects.get(id=presentation_id)
            presentation.delete()
            return True
        except ObjectDoesNotExist:
            logger.warning(f"Presentation with id {presentation_id} does not exist.")
            return False
        except Exception as e:
            logger.error(f"Error deleting presentation with id {presentation_id}: {e}")
            return False

    @staticmethod
    def get_all_presentations():
        try:
            return Presentation.objects.all()
        except Exception as e:
            logger.error(f"Error retrieving all presentations: {e}")
            return None
