from django.db import models


class Users(models.Model):
    # alternate primary key
    username = models.TextField()

    password_hash = models.TextField()
    access_token = models.TextField(null=True)
