from django.db import models
from models_constants import ON_DELETE_BEHAVIOUR
from user import User


class Presentation(models.Model):
    user_id = models.ForeignKey(User, on_delete=ON_DELETE_BEHAVIOUR)
    title = models.TextField()
    file_path = models.TextField()

    def __str__(self):
        return self.title
