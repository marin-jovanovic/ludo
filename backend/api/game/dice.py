from random import SystemRandom


def get_dice_result(number_of_sides):
    crypto_generator_object = SystemRandom()
    return crypto_generator_object.randrange(
        number_of_sides) + 1
