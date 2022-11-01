from random import SystemRandom

from backend.api.game.resources import get_config


def get_dice_result():
    crypto_generator_object = SystemRandom()
    return crypto_generator_object.randrange(
        get_config()['dice number of sides']) + 1