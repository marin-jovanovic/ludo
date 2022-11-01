import sys
from collections import defaultdict

from backend.api.game.dice import get_dice_result
from backend.api.game.log import construct_roll, move_token
from backend.api.game.log import log_won
from backend.api.game.order import determine_order
from backend.api.game.pre import get_start_pool_preprocessor, \
    player_moves_preprocessor
from backend.api.game.resources import get_config

# todo if user gets 5 but there are only 3 spaces left then move
#   do not wait till user gets 3 (for placing token in win position)
todo_move_to_last_if_exceed = True


# done
# action eat
# if in end pool can not be eaten

# todo
# move max to destination, not over

class Board:

    def __init__(self, players, start_pool):
        self.players = players

        self.board_state = defaultdict(lambda: defaultdict(set))

        for p_id, p in self.players.items():
            for t_id, token in p.items():
                token_start_position = start_pool[p_id][token.id_]

                row = token_start_position.row
                column = token_start_position.column

                self.board_state[row][column].add(token)

    def has_any_on_board(self, player):
        return self.__any_driver(player, choice_start_pool_or_board=False)

    def any_in_start_pool(self, player):
        return self.__any_driver(player, choice_start_pool_or_board=True)

    def __any_driver(self, player, choice_start_pool_or_board):
        for token_id, token in self.players[player].items():

            if choice_start_pool_or_board:
                if token.is_in_starting_pool:
                    return True

            else:
                if not token.is_in_starting_pool and not token.is_token_at_destination_pool():
                    return True

        return False

    def __get_from(self, player, choice_start_pool_or_board):
        r = {}

        for token_id, token in self.players[player].items():
            if self.is_token_at_destination(player, token_id):
                continue

            if choice_start_pool_or_board:
                if token.is_in_starting_pool:
                    r[token_id] = token

            else:
                if not token.is_in_starting_pool:
                    r[token_id] = token

        return r

    def get_from_start_pool(self, player):
        return self.__get_from(player, choice_start_pool_or_board=True)

    def get_from_board(self, player, dice_result=None):
        """
        return all tokens on board

        """

        if not dice_result:
            return self.__get_from(player, choice_start_pool_or_board=False)

        else:
            r = self.__get_from(player, choice_start_pool_or_board=False)

            ret = {}

            for token_id, token in r.items():
                if token.current_position + dice_result <= token.destination_position:
                    ret[token_id] = token

            return ret

    def is_token_at_destination(self, player_id, token_id):
        return self.players[player_id][token_id].is_token_at_destination_pool()

    def is_game_won(self):
        winning_order = []

        for p_id, p in self.players.items():
            all_at_destination = True

            for t_id, token in p.items():
                if not token.is_token_at_destination_pool():
                    all_at_destination = False
                    break

            if all_at_destination:
                winning_order.append(p_id)

        return winning_order

    def move_token(self, player, token_id, step):
        # for token_id, token in self.players[player].items():
        #     if tok
        #
        token = self.players[player][token_id]

        if token.is_in_starting_pool:
            pass
            # print("before", token)
            # print("moving only one position")

            #     step must be one

            # print(f"{step=}")

            if step != 1:
                print("integrity error: step must be 1")
                sys.exit(-1)

        else:

            # print(f"{token.current_position=}")
            # print(f"{step=}")
            # print(f"{token.destination_position=}")

            if not (
                    token.current_position + step <= token.destination_position):
                print(token)
                print(f"{token.current_position=}")
                print(f"{step=}")
                print(f"{token.destination_position=}")
                print("integrity err")
                sys.exit(-1)

        token_global_position = self.players[player][
            token_id].normalize_position()

        row = token_global_position.row
        column = token_global_position.column

        # remove this token
        to_remove = set()
        for token in self.board_state[row][column]:
            if token.id_ == token_id and token.owner == player:
                to_remove.add(token)

        for i in to_remove:
            self.board_state[row][column].remove(i)

        # this token: update players
        self.players[player][token_id].update_position(step)

        token_global_position = self.players[player][
            token_id].normalize_position()

        row = token_global_position.row
        column = token_global_position.column

        to_ret = []
        # eat enemy tokens at destination
        if self.board_state[row][column]:
            to_remove = set()
            # someone is here

            for i in self.board_state[row][column]:

                if not i.owner == player:
                    # my token

                    if not i.is_token_at_destination_pool():
                        # game rule, can not eat tokens at destination pool
                        # someone elses token

                        to_remove.add(i)

            for i in to_remove:
                self.board_state[row][column].remove(i)
                r = self.players[i.owner][i.id_].move_to_start_position()
                to_ret.append({"player": i.owner, "token": i.id_,
                               "revert count": r["reverted"]})

        # add this token
        self.board_state[row][column].add(self.players[player][token_id])

        return {
            "eaten": to_ret,
            "won order": self.is_game_won()
        }

    def print_board_state(self):

        for row, m_c_to_tokens in self.board_state.items():
            for column, tokens in m_c_to_tokens.items():
                print(row, column, [str(i) for i in tokens])
        print()


class Player:

    def __init__(self, tokens):
        self.tokens = tokens


class Token:

    def __init__(
            self,
            start_tile,
            id_,
            destination_position,
            owner,
            moves
    ):
        self.id_ = id_

        self.current_position = None
        # self.current_tile = start_tile

        # todo logic when is in it

        # todo in starting pool there is only one place where token can be
        # token can not be placed in multiple places in starting pool
        self.is_in_starting_pool = True
        self.start_tile = start_tile

        self.destination_position = destination_position
        # self.destination_tile = None
        self.is_at_destination = False

        self.owner = owner
        self.moves = moves

    # def __eq__(self, other):
    #     """Overrides the default implementation"""
    #     if isinstance(other, Token):
    #         return self.id_ == other.id_ and self.owner == other.owner
    #     return False

    def normalize_position(self):

        if self.is_in_starting_pool:
            return self.start_tile

        return self.moves[self.current_position]

    def is_token_at_destination_pool(self):
        return self.is_at_destination

    def move_to_start_position(self):

        if self.is_at_destination:
            print("can not move from destination to start")
            sys.exit(-1)

        self.is_in_starting_pool = True

        r = -self.current_position

        self.current_position = None

        return {
            "reverted": r
        }

    def update_position(self, step):
        if self.is_in_starting_pool:
            if step > 0:
                self.is_in_starting_pool = False

                # todo check: token will be placed on this tile when moved out
                #   out of starting pool
                self.current_position = -1

            else:
                # todo
                print("step error")
                sys.exit(-1)

        if self.is_at_destination:
            print('at destination, can not move')
            sys.exit(-1)

        self.current_position += step

        # todo remove this check, it shouldnt be >, just =
        if self.current_position >= self.destination_position:
            self.current_position = self.destination_position
            # self.current_tile = self.desti
            self.set_is_at_destination()

    def set_is_at_destination(self):
        # print(self.normalize_position())
        self.is_at_destination = True

    def __str__(self):
        return f'{self.owner=}, {self.id_=}'

    # todo destination same or ascending
    # f_same_destination = get_config()["flag: same destination"]
    #
    # if f_same_destination:
    #     # print('same destination')
    #     players_id = [i for i in range(get_config()['number of players'])]
    #     # print(players_id)
    #
    #     # p = {i: for i in players_id}
    #
    # else:
    #     # print('not same destination')
    #     # print("not implemented")
    #     sys.exit(-1)


class Level:

    def __init__(self):

        already_won = []

        self.log = []

        game_conf = get_config()

        # todo num of play
        order = determine_order(
            game_conf['number of players'],
            game_conf['choice: highest; order'],
            game_conf['choice: clockwise; anticlockwise'],
            game_conf['flag: tie in order'],
        )

        self.log += order

        goes_list = []

        for i in self.log:
            if i["action"] == "goes":
                goes_list.append(i["player"])

                if len(goes_list) == game_conf['number of players']:
                    break

        m_player_to_moves = player_moves_preprocessor()

        start_pool = get_start_pool_preprocessor()

        players = {}
        for player_id in range(get_config()["number of players"]):
            tokens = {}

            # todo assumption all tokens need to reach same destination position
            destination_position = max(m_player_to_moves[player_id])

            for token_id in range(get_config()['tokens per player']):
                start_tile = start_pool[player_id][token_id]

                tokens[token_id] = Token(
                    owner=player_id,
                    id_=token_id,

                    start_tile=start_tile,

                    destination_position=destination_position,
                    moves=m_player_to_moves[player_id]
                )

            players[player_id] = tokens

        b = Board(players=players, start_pool=start_pool)

        max_result = 6

        self.driver(already_won, b, game_conf, goes_list, max_result,
                    start_pool)

    def driver(
            self, already_won, b, game_conf, goes_list, max_result, start_pool):
        while True:

            for player_id in goes_list:

                can_roll_again = True

                while can_roll_again:

                    roll_result = get_dice_result()

                    can_roll_again = roll_result == max_result

                    self.log.append(
                        construct_roll(player=player_id, roll=roll_result))

                    can_move_from_start_pool = roll_result == max_result and \
                                               b.any_in_start_pool(
                                                   player=player_id)

                    # todo add here restriction for destination
                    can_move_on_board = b.has_any_on_board(player=player_id)

                    if can_move_from_start_pool and can_move_on_board:

                        to_choose = {}

                        in_start_pool = b.get_from_start_pool(player_id)

                        for token_id, token in in_start_pool.items():
                            to_choose[token_id] = token
                        for token_id, token in b.get_from_board(
                                player=player_id,
                                dice_result=roll_result).items():
                            to_choose[token_id] = token

                        for token_id, token in to_choose.items():
                            # todo   # print("player choosing first option")

                            step = 1 if token_id in start_pool else roll_result

                            t = choose(b, self.log, player_id, step, token_id,
                                       already_won)

                            for j in t["won"]:
                                already_won.append(j)

                            break

                    elif can_move_from_start_pool:
                        sp = b.get_from_start_pool(player_id)

                        is_auto = True
                        if is_auto:
                            for token_id, token in sp.items():
                                t = choose(b, self.log, player_id, 1, token_id,
                                           already_won)
                                for j in t["won"]:
                                    already_won.append(j)
                                break

                    elif can_move_on_board:
                        to_choose = {}

                        for token_id, token in b.get_from_board(
                                player=player_id,
                                dice_result=roll_result).items():
                            to_choose[token_id] = token

                        for token_id, token in to_choose.items():
                            # todo player choose
                            t = choose(b, self.log, player_id, roll_result,
                                       token_id,
                                       already_won)
                            for j in t["won"]:
                                already_won.append(j)
                            break

                    if game_conf['number of players'] == len(already_won) + 1:
                        print("last player is loser")
                        print("no need to play game with only him")

                        return

    def get_log(self):
        return self.log


def generate_whole_game():
    level = Level()
    return level.get_log()

    #
    # # todo number_of_players = game_conf['number of players']
    #
    # already_won = []
    #
    # log = []
    #
    # game_conf = get_config()
    #
    # # todo num of play
    # order = determine_order(
    #     game_conf['number of players'],
    #     game_conf['choice: highest; order'],
    #     game_conf['choice: clockwise; anticlockwise'],
    #     game_conf['flag: tie in order'],
    # )
    #
    # log += order
    #
    # goes_list = []
    #
    # for i in log:
    #     if i["action"] == "goes":
    #         goes_list.append(i["player"])
    #
    #         if len(goes_list) == game_conf['number of players']:
    #             break
    #
    # m_player_to_moves = player_moves_preprocessor()
    #
    # start_pool = get_start_pool_preprocessor()
    #
    # players = {}
    # for player_id in range(get_config()["number of players"]):
    #     tokens = {}
    #
    #     # todo assumption all tokens need to reach same destination position
    #     destination_position = max(m_player_to_moves[player_id])
    #
    #     for token_id in range(get_config()['tokens per player']):
    #         start_tile = start_pool[player_id][token_id]
    #
    #         tokens[token_id] = Token(
    #             owner=player_id,
    #             id_=token_id,
    #
    #             start_tile=start_tile,
    #
    #             destination_position=destination_position,
    #             moves=m_player_to_moves[player_id]
    #         )
    #
    #     players[player_id] = tokens
    #
    # b = Board(players=players, start_pool=start_pool)
    #
    # max_result = 6
    #
    # game_done = False
    # while True:
    #
    #     for player_id in goes_list:
    #
    #         can_roll_again = True
    #
    #         while can_roll_again:
    #
    #             roll_result = get_dice_result()
    #
    #             can_roll_again = roll_result == max_result
    #
    #             log.append(construct_roll(player=player_id, roll=roll_result))
    #
    #             can_move_from_start_pool = roll_result == max_result and \
    #                                    b.any_in_start_pool(
    #                 player=player_id)
    #
    #             # todo add here restriction for destination
    #             can_move_on_board = b.has_any_on_board(player=player_id)
    #
    #             if can_move_from_start_pool and can_move_on_board:
    #
    #                 to_choose = {}
    #
    #                 in_start_pool = b.get_from_start_pool(player_id)
    #
    #                 for token_id, token in in_start_pool.items():
    #                     to_choose[token_id] = token
    #                 for token_id, token in b.get_from_board(
    #                         player=player_id, dice_result=roll_result).items():
    #                     to_choose[token_id] = token
    #
    #                 for token_id, token in to_choose.items():
    #                     # todo   # print("player choosing first option")
    #
    #                     step = 1 if token_id in start_pool else roll_result
    #
    #                     t = choose(b, log, player_id, step, token_id,
    #                                already_won)
    #
    #                     for j in t["won"]:
    #                         already_won.append(j)
    #
    #                     break
    #
    #             elif can_move_from_start_pool:
    #                 sp = b.get_from_start_pool(player_id)
    #
    #                 is_auto = True
    #                 if is_auto:
    #                     for token_id, token in sp.items():
    #                         t = choose(b, log, player_id, 1, token_id,
    #                                    already_won)
    #                         for j in t["won"]:
    #                             already_won.append(j)
    #                         break
    #
    #             elif can_move_on_board:
    #                 # print("todo move board")
    #                 to_choose = {}
    #
    #                 for token_id, token in b.get_from_board(
    #                         player=player_id, dice_result=roll_result).items():
    #                     to_choose[token_id] = token
    #
    #                 for token_id, token in to_choose.items():
    #                     # todo
    #                     # print("player choosing first option")
    #                     # print(token_id, token)
    #                     t = choose(b, log, player_id, roll_result, token_id,
    #                                already_won)
    #                     for j in t["won"]:
    #                         already_won.append(j)
    #                     break
    #
    #             if game_conf['number of players'] == len(already_won) + 1:
    #                 print("last player is loser, no need to play game with only him")
    #                 game_done = True
    #                 break
    #
    #         if game_done:
    #             break
    #
    #     if game_done:
    #         break
    #
    # # b.print_board_state()
    # # print()
    #
    # return log


def main():
    log = generate_whole_game()

    for i in log:
        print(i)


from backend.api.game.log import log_eat_token


def choose(b, log, player_id, roll_result, token_id, already_won):
    """
    wrapper for moving token

    """

    t = b.move_token(player=player_id, token_id=token_id,
                     step=roll_result)

    eaten = t["eaten"]
    gw = t["won order"]

    log.append(move_token(
        player=player_id,
        token=token_id,
        step=roll_result
    ))

    for i in eaten:
        log.append(log_eat_token(
            player=i["player"],
            token=i["token"],
        ))

    for i in gw:
        if i not in already_won:
            log.append(log_won(player=i))

    return {"won": gw}


if __name__ == '__main__':
    main()
