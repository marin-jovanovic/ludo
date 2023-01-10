from random import SystemRandom

from backend.api.cqrs_q.level_config import get_config


def get_dice_result(number_of_sides):
    crypto_generator_object = SystemRandom()
    return crypto_generator_object.randrange(
        number_of_sides) + 1
