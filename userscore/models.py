from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100, default="", unique=True)
    score = models.FloatField(default=0)
    games_played = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Levels(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    level_score = models.FloatField(default=0)
    level_id = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.user.name


