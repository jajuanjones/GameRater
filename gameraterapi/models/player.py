from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    """This class will initialize a player model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(default=None)