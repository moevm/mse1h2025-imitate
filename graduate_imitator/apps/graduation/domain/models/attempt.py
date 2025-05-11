from django.db import models
from .models_constants import ON_DELETE_BEHAVIOUR
from .user import User
from .presentation import Presentation


class Attempt(models.Model):
    user_id = models.ForeignKey(User, on_delete=ON_DELETE_BEHAVIOUR)
    presentation_id = models.ForeignKey(Presentation, on_delete=ON_DELETE_BEHAVIOUR)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    score = models.IntegerField()
    completed = models.BooleanField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time} {'Completed' if self.completed else 'Not completed'}"