from django.core.exceptions import ObjectDoesNotExist
from ..models.user import User
import logging

logger = logging.getLogger(__name__)


class UserRepository:
    @staticmethod
    def create_user(username, password_hash):
        try:
            user = User(username=username, password_hash=password_hash)
            user.save()
            return user
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_user_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            logger.warning(f"User with id {user_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error retrieving user by id: {e}")
            return None

    @staticmethod
    def get_user_by_username(username):
        try:
            return User.objects.get(username=username)
        except ObjectDoesNotExist:
            logger.warning(f"User with username {username} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error retrieving user by username: {e}")
            return None

    @staticmethod
    def update_user_password(user_id, new_password_hash):
        try:
            user = User.objects.get(id=user_id)
            user.password_hash = new_password_hash
            user.save()
            return user
        except ObjectDoesNotExist:
            logger.warning(f"User with id {user_id} does not exist.")
            return None
        except Exception as e:
            logger.error(f"Error updating user password: {e}")
            return None

    @staticmethod
    def delete_user(user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except ObjectDoesNotExist:
            logger.warning(f"User with id {user_id} does not exist.")
            return False
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return False

    @staticmethod
    def get_all_users():
        try:
            return User.objects.all()
        except Exception as e:
            logger.error(f"Error retrieving all users: {e}")
            return None
