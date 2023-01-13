from django.apps import apps
from django.db import models

from backend.api.model.level import get_level_model_as_string


class GameLog(models.Model):
    # primary key
    # id

    game = models.ForeignKey(
        get_level_model_as_string(),
        on_delete=models.SET_NULL,
        null=True
    )

    instruction_id = models.IntegerField()

    # pl

    # why not foreign key to user
    player = models.IntegerField()

    token = models.IntegerField(null=True)
    dice_result = models.IntegerField(null=True)

    # if previous null
    # todo extract in separate table
    action = models.TextField()

    # performed = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game', 'instruction_id'],
                                    name='game instruction_id pk')
        ]


#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['game', 'instruction_id'],
#                                     name='game instruction_id pk')
#         ]

def get_level_log_model():
    return apps.get_model(get_level_log_model_as_string())


def get_level_log_model_as_string():
    return "api.gamelog"
