import sys
from collections import defaultdict

from backend.api.game.dice import get_dice_result
from backend.api.game.log import construct_roll, move_token, log_won, log_eat_token
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
# move max to destination, not over
# jump one by one

# todo

class Board:

    def __init__(self, players, start_pool, m_player_to_moves):

        self.level_state = {
            "status": {},
            "players": {}
        }

        for p_id, p in players.items():

            self.level_state["players"][p_id] = {
                "tokens": {},
                "states": m_player_to_moves[p_id]
            }

            for t_id, token in p.items():
                self.level_state["players"][p_id]["tokens"][t_id] = token


        # for p_id, pl in self.level_state["players"].items():
        #     for s_id, state in pl["states"].items():
        #         print(p_id, s_id, state)

        # print("--")
        #
        self.players = self.level_state["players"]
        #
        # self.tokens = {}
        #
        # self.board_state = defaultdict(lambda: defaultdict(set))
        #
        # for p_id, p in self.players.items():
        #     for t_id, token in p.items():
        #         # fixme this is needed if loading mid game
        #         # token_start_position = start_pool[p_id][t_id]
        #         # row = token_start_position.row
        #         # column = token_start_position.column
        #
        #         row, column = self.players[p_id][t_id].get_row_column()
        #
        #         self.board_state[row][column].add(token)
        #
        #         self.tokens[t_id] = token

    def has_any_on_board(self, player):
        """return True if @player has any tokens in non-start pool"""

        return self.__any_driver(player, pools=[get_pool("live"),get_pool("safe")])

    def any_in_start_pool(self, player):
        """return True if @player has any tokens in live pool"""

        return self.__any_driver(player, pools=[get_pool("start")])

    def __any_driver(self, player, pools):
        """internal driver for checking if @player has any tokens in @choice_start_pool_or_board"""

        for token_id, token in self.players[player]["tokens"].items():

            if any(token.pool == p for p in pools):
                return True

        return False

    def __get_from(self, player_id, pools):
        """
        filter @player
        filter @pools
        filter token not at destination

        return {
            token_id -> token
        }

        """

        r = {}

        for token_id, token in self.players[player_id]["tokens"].items():
            if self.is_token_at_destination(player_id, token_id):
                continue

            if any(token.pool == p for p in pools):
                r[token_id] = token

        return r

    def get_from_start_pool(self, player_id):
        "return dict {token_id -> token}"

        return self.__get_from(player_id, pools=[get_pool("start")])

    def get_from_board(self, player, dice_result=None):
        """
        select tokens
        from board

        filter player_id
        filter pool = live | safe

        filter current_state + dice_result in states

        return all tokens on board
        {token_id -> token}

        """

        if not dice_result:
            return self.__get_from(player, pools=[get_pool("start")])

        else:
            r = self.__get_from(player, pools=[get_pool("live"), get_pool("safe")])

            ret = {}

            for token_id, token in r.items():

                if token.current_state + dice_result not in self.level_state["players"][player]["states"]:
                    continue

                ret[token_id] = token

            return ret

    def is_token_at_destination(self, player_id, token_id):
        """wrapper"""
        return self.players[player_id]["tokens"][token_id].get_is_at_destination()

    def any_movable(self, player_id):

        return len(self.get_movable(player_id)) != 0


    def get_movable(self, player_id):
        """
        filter player_id
        filter tokens in live or safe pool
        filter tokens not at_destination

        """

        pools = [get_pool("live"), get_pool("safe")]

        tokens = {}

        for token_id, t in self.players[player_id]["tokens"].items():

            if not any(t.pool == p for p in pools):
                continue

            if t.get_is_at_destination():
                continue

            tokens[token_id] = t

        return tokens

    def is_game_won(self):
        winning_order = []

        for p_id, p in self.players.items():
            all_at_destination = True

            for t_id, token in p["tokens"].items():
                if not self.is_token_at_destination(player_id=p_id, token_id=t_id):
                    all_at_destination = False
                    break

            if all_at_destination:
                winning_order.append(p_id)

        return winning_order

    def move_token(self, player_id, token_id, step):

        token = self.players[player_id]["tokens"][token_id]

        if token.pool == get_pool("start"):

            if step != 1:
                print("[err] integrity error: step must be 1")
                sys.exit(-1)

        is_moved = self.players[player_id]["tokens"][token_id].move_forward(
            step=step,
            states=self.level_state["players"][player_id]["states"]
        )

        if not is_moved:
            print(f"[err] can not move {player_id=} {token_id=}")
            # return

        # todo eating

        # todo set flags for token, chech that

        # row, column = self.players[player_id]["tokens"][token_id].get_row_column()

        # remove token from board_state
        # update token state, x_y
        # check eating

        # self.board_state[row][column].remove(self.tokens[token_id])

        # this token: update players
        # self.players[player_id]["tokens"][token_id].update_position(step)

        # row, column = self.players[player_id]["tokens"][token_id].get_row_column()
        #
        # to_ret = []
        # # eat enemy tokens at destination
        # if self.board_state[row][column]:
        #     to_remove = set()
        #     # someone is here
        #
        #     for i in self.board_state[row][column]:
        #
        #         if not i.owner == player_id:
        #             # my token
        #
        #             if not i.is_token_at_destination_pool():
        #                 # game rule, can not eat tokens at destination pool
        #                 # someone elses token
        #
        #                 to_remove.add(i)
        #
        #     for i in to_remove:
        #         self.board_state[row][column].remove(i)
        #         r = self.players[i.owner][i.id_].move_to_start_position()
        #         to_ret.append({"player": i.owner, "token": i.id_,
        #                        "revert count": r["reverted"]})

        # add this token
        # self.board_state[row][column].add(self.players[player_id]["tokens"][token_id])

        return {
            "eaten": [],
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


def get_pool(type_):
    """
    vals are those from Fe generating board part
    """


    return {
        "start": 1,
        "live": 2,
        "safe": 3
    }[type_]


class Token:

    def __init__(
            self,
            start_state,
            start_x_y,
    ):

        self.start_state = start_state
        self.start_x_y = start_x_y

        self.current_state = start_state
        self.current_x_y = start_x_y

        self.is_at_destination = False

        self.pool = get_pool("start")

    def get_row_column(self):
        return self.start_x_y.row, self.start_x_y.column

    def set_at_destination(self):
        self.is_at_destination = True

    def get_is_at_destination(self):
        return self.is_at_destination

    def restart(self):

        if self.get_is_at_destination():
            print("[err] token at destination")
            sys.exit(-1)

        self.current_state = self.start_state
        self.current_x_y = self.start_x_y
        self.pool = get_pool("start")

    def move_forward(self, step, states):
        """
        if step is to big, exception will be thrown, no need to check now

        """

        if step <= 0:
            print("[err] step 0")
            sys.exit(-1)

        if self.is_at_destination:
            print('[err] at destination, can not move')
            sys.exit(-1)

        if self.pool == get_pool("start"):

            # todo dehardcode
            self.current_state = 0
            self.current_x_y = self.start_x_y
            self.pool = get_pool("live")

        elif self.pool == get_pool("live"):

            self.current_state += step
            try:

                self.current_x_y = states[self.current_state]

            except KeyError:
                print("[err] trying to jump out of board")
                return False

            if self.current_x_y.type == get_pool("safe"):
                self.pool = self.current_x_y

        elif self.pool == get_pool("safe"):

            self.current_state += step
            self.current_x_y = states[self.current_state]

        else:
            print("[err] unknown pool")
            return False

        return True


class Level:

    def __init__(self, log=None):
        game_conf = get_config()
        max_result = 6

        # if mid game
        if log:
            self.log = log
        else:
            self.log = determine_order(
                game_conf['number of players'],
                game_conf['choice: highest; order'],
                game_conf['choice: clockwise; anticlockwise'],
                game_conf['flag: tie in order'],
            )

        for i in game_conf.items():
            print(i)

        player_order = self.goes_list_driver(game_conf)

        m_player_to_moves = player_moves_preprocessor()

        start_pool = get_start_pool_preprocessor()


        players = {}

        default_start_state = -1

        for player_id in range(get_config()["number of players"]):
            tokens = {}

            for token_id in range(get_config()['tokens per player']):
                start_tile = start_pool[player_id][token_id]


                tokens[token_id] = Token(
                    start_state=default_start_state,
                    start_x_y=start_tile,
                )

            players[player_id] = tokens
        # in log is determined order

        already_won = []
        board = Board(players=players, start_pool=start_pool, m_player_to_moves = m_player_to_moves)

        # self.manual_driver(already_won, board, game_conf, player_order, max_result,
        #                    start_pool)

        self.auto_driver(already_won, board, game_conf, player_order, max_result,
                         start_pool)

    def goes_list_driver(self, game_conf) -> list:
        """
        return [0, 2, 1]
        """

        goes_list = []
        for i in self.log:
            if i["action"] == "goes":
                goes_list.append(i["player"])

                if len(goes_list) == game_conf['number of players']:
                    break
        return goes_list

    def manual_driver(
            self, already_won, board, game_conf, goes_list, max_result, start_pool):

        while True:

            for player_id in goes_list:

                can_roll_again = True

                while can_roll_again:

                    roll_result = get_dice_result()

                    can_roll_again = roll_result == max_result

                    self.log.append(
                        construct_roll(player=player_id, roll=roll_result))

                    can_move_from_start_pool = roll_result == max_result and \
                                               board.any_in_start_pool(
                                                   player=player_id)

                    # todo add here restriction for destination
                    can_move_on_board = board.has_any_on_board(player=player_id)

                    if can_move_from_start_pool and can_move_on_board:

                        to_choose = {}

                        in_start_pool = board.get_from_start_pool(player_id)

                        for token_id, token in in_start_pool.items():
                            to_choose[token_id] = token
                        for token_id, token in board.get_from_board(
                                player=player_id,
                                dice_result=roll_result).items():
                            to_choose[token_id] = token

                        if len(to_choose) == 1:
                            for token_id, token in to_choose.items():

                                step = 1 if token_id in start_pool else roll_result

                                t = choose(board, self.log, player_id, step, token_id,
                                           already_won)

                                for j in t["won"]:
                                    already_won.append(j)

                                break

                        else:
                            return

                    elif can_move_from_start_pool:
                        sp = board.get_from_start_pool(player_id)

                        is_auto = True
                        if is_auto:
                            for token_id, token in sp.items():
                                t = choose(board, self.log, player_id, 1, token_id,
                                           already_won)
                                for j in t["won"]:
                                    already_won.append(j)
                                break

                    elif can_move_on_board:
                        to_choose = {}

                        for token_id, token in board.get_from_board(
                                player=player_id,
                                dice_result=roll_result).items():
                            to_choose[token_id] = token

                        if len(to_choose) == 1:
                            for token_id, token in to_choose.items():
                                t = choose(board, self.log, player_id, roll_result,
                                           token_id,
                                           already_won)
                                for j in t["won"]:
                                    already_won.append(j)
                                break

                        else:
                            return

                    if game_conf['number of players'] == len(already_won) + 1:
                        print("last player is loser")
                        print("no need to play game with only him")

                        return


    def auto_driver(
        self,
            already_won,
            board,
            game_conf,
            goes_list,
            max_result,
            start_pool
    ):

        ttl = 30

        while True:
            ttl -= 1
            if ttl < 0:
                break

            for player_id in goes_list:

                can_roll_again = True

                while can_roll_again:

                    roll_result = get_dice_result()

                    can_roll_again = roll_result == max_result

                    self.log.append(
                        construct_roll(player=player_id, roll=roll_result))

                    can_move_from_start_pool = roll_result == max_result and \
                                               board.any_in_start_pool(
                                                   player=player_id)

                    # todo add here restriction for destination
                    can_move_on_board = board.has_any_on_board(player=player_id) and board.any_movable(player_id=player_id)

                    if can_move_from_start_pool and can_move_on_board:

                        to_choose = {}

                        in_start_pool = board.get_from_start_pool(player_id)

                        for token_id, token in in_start_pool.items():
                            to_choose[token_id] = token

                        for token_id, token in board.get_from_board(
                                player=player_id,
                                dice_result=roll_result).items():
                            to_choose[token_id] = token

                        for token_id, token in to_choose.items():
                            # todo   # print("player choosing first option")

                            step = 1 if token_id in start_pool else roll_result


                            # print(1)
                            t = choose(board, self.log, player_id, step, token_id,
                                       already_won)

                            for j in t["won"]:
                                already_won.append(j)

                            break

                    elif can_move_from_start_pool:
                        sp = board.get_from_start_pool(player_id)

                        is_auto = True
                        if is_auto:
                            for token_id, token in sp.items():
                                # print(2)
                                t = choose(board, self.log, player_id, 1, token_id,
                                           already_won)
                                for j in t["won"]:
                                    already_won.append(j)
                                break

                    elif can_move_on_board:
                        to_choose = {}

                        # for token_id, token in board.get_movable(player_id=player_id):
                            # print()

                        for token_id, token in board.get_from_board(
                                player=player_id,
                                dice_result=roll_result).items():
                            to_choose[token_id] = token

                        for token_id, token in to_choose.items():
                            # todo player choose
                            # print(3)
                            t = choose(board, self.log, player_id, roll_result,
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


def generate_start():
    level = Level()
    return level.get_log()


def choose(board, log, player_id, roll_result, token_id, already_won):
    """
    wrapper for moving token

    """

    t = board.move_token(player_id=player_id, token_id=token_id,
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


def generate_whole_game():
    level = Level()
    return level.get_log()


def main():
    log = generate_whole_game()

    for i in log:
        print(i)

if __name__ == '__main__':
    main()
