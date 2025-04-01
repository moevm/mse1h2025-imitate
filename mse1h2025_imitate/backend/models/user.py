from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    password_hash = models.TextField()
    created_at = models.DateField()

    def __str__(self):
        return self.username
