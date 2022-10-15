from django.db import models


class Users(models.Model):
    username = models.TextField()
    password_hash = models.TextField()
