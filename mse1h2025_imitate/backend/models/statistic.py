from django.db import models
from models_constants import ON_DELETE_BEHAVIOUR
from user import User


class Statistic(models.Model):
    user_id = models.ForeignKey(User, on_delete=ON_DELETE_BEHAVIOUR)
    total_attempts = models.IntegerField()
    avg_score = models.FloatField()
    questions_answered = models.IntegerField()
    performance_data = models.JSONField()

    def __str__(self):
        return f"{self.user_id} - {self.avg_score}"
