from django.db import models
from models_constants import ON_DELETE_BEHAVIOUR
from attempt import Attempt
from question import Question


class Answer(models.Model):
    attempt_id = models.ForeignKey(Attempt, on_delete=ON_DELETE_BEHAVIOUR)
    question_id = models.ForeignKey(Question, on_delete=ON_DELETE_BEHAVIOUR)
    user_answer = models.TextField()
    answered_at = models.DateField()
    accuracy_score = models.FloatField()
    analysis_results = models.JSONField()

    def __str__(self):
        return self.user_answer
