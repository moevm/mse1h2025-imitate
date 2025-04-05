from django.db import models


class Question(models.Model):
    question_text = models.TextField()
    category = models.CharField(max_length=100)
    difficulty_level = models.IntegerField()
    keywords = models.JSONField()

    def __str__(self):
        return self.question_text
