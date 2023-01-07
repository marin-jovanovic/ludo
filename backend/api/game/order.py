import sys

from backend.api.cqrs_q.level_config import get_config
from backend.api.game.dice import get_dice_result
from backend.api.game.log import construct_goes, construct_roll, construct_tie


def determine_order(
        number_of_players, choice_highest_or_order,
        choice_clockwise_or_anticlockwise, f_tie_in_order):
    def driver(
            number_of_players, choice_highest_or_order,
            choice_clockwise_or_anticlockwise):
        # pre

        # global, pass as arg
        roll_history = []

        rollers = [i for i in range(number_of_players)]

        # driver

        while True:
            if len(rollers) == 1:
                roll_history.append(construct_goes(rollers[0]))
                return roll_history

            current_iteration_roll_history = []
            for player in rollers:
                r = get_dice_result()
                pr = {'player': player, 'dice_result': r}

                roll_history.append(construct_roll(player, r))

                current_iteration_roll_history.append(pr)

            while True:

                if len(current_iteration_roll_history) == 1:
                    roll_history.append(construct_goes(
                        current_iteration_roll_history[0]['player']))

                    return roll_history

                is_same_max, max_r_obj = find_max(
                    current_iteration_roll_history)

                if is_same_max:
                    roll_history.append(construct_tie())
                    break

                winner = max_r_obj['player']
                if choice_highest_or_order:
                    for i, v in enumerate(current_iteration_roll_history):
                        if max_r_obj['player'] == v['player']:

                            for j in rollers:
                                if choice_clockwise_or_anticlockwise:
                                    c = (i + j) % len(
                                        current_iteration_roll_history)
                                else:
                                    c = (i - j) % len(
                                        current_iteration_roll_history)

                                roll_history.append(construct_goes(c))

                            return roll_history

                roll_history.append(construct_goes(winner))
                rollers.remove(max_r_obj['player'])
                current_iteration_roll_history.remove(max_r_obj)

    r = driver(number_of_players, choice_highest_or_order,
               choice_clockwise_or_anticlockwise)

    if number_of_players > get_config()['dice number of sides']:
        print('err')
        sys.exit(-1)

    if not f_tie_in_order:
        while True:
            is_present = False
            for i in r:
                if i["action"] == "tie":
                    is_present = True
                    break

            if is_present:
                r = driver(number_of_players, choice_highest_or_order,
                           choice_clockwise_or_anticlockwise)

            else:
                break

    return r


def find_max(current_iteration_roll_history):
    is_same_max = False
    max_r_obj = None
    for i in current_iteration_roll_history:
        if not max_r_obj or i['dice_result'] > max_r_obj['dice_result']:
            is_same_max = False
            max_r_obj = i
        elif i['dice_result'] == max_r_obj['dice_result']:
            is_same_max = True

    return is_same_max, max_r_obj
