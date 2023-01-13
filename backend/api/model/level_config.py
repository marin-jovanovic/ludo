from django.apps import apps
from django.db import models


class LevelConfig(models.Model):
    number_of_users = models.IntegerField(default=4)
    tokens_per_user = models.IntegerField(default=4)
    dice_number_of_sides = models.IntegerField(default=6)

    # assumption: talking for each player individually
    # if True: all tokens must reach the same destination
    # else: each token has it unique(multiple can go to same destination, but it is not a rule)
    # destination location
    same_destination = models.BooleanField(default=True)

    # highest: highest goes first and then clockwise or anticlockwise (6, right, right, right)
    # order: 1st, 2nd, 3rd, 4th highest roll (6, 3, 2, 1)
    highest_order = models.BooleanField(default=True)

    # if highest then in which direction
    # clockwise if True else anticlockwise
    clockwise = models.BooleanField(default=False)

    # when rolling dice to see who goes first
    # skip if tie will occur
    tie_in_order = models.BooleanField(default=False)


def get_level_config_model():
    return apps.get_model(get_level_config_model_as_string())


def get_level_config_model_as_string():
    return "api.levelconfig"
