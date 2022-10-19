from django.db import models

class User(models.Model):

    class Role(models.IntegerChoices):
        AGGREGATOR = 1
        BUILDING_MANAGER = 2
        AGGREGATOR_AND_BUILDING_MANAGER = 3

    role_id = models.IntegerField(choices=Role.choices)
    password = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
