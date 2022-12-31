import sys
from collections import defaultdict

from backend.api.game.dice import get_dice_result
from backend.api.game.log import construct_roll, move_token, log_won, \
    log_eat_token
from backend.api.game.order import determine_order
from backend.api.game.pool import get_pool, is_valid_pool
from backend.api.game.pre import get_destination_pool
from backend.api.game.pre import player_moves_preprocessor
from backend.api.game.resources import get_config



# todo loading mid game config, content
# todo manual driver

def log_err(content):
    print(f"[err] {content}")


class Board:

    def __init__(
            self, players, m_player_to_moves, game_conf, default_start_state):

        self.default_start_state = default_start_state

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

        self.max_result = game_conf["dice number of sides"]

    def get_from_start_pool(self, player_id, dice_result):
        """
        return dict {token_id -> token}
        assumption:
            moving by 1 if in start pool,
            will not jump out of board
        """

        if dice_result != self.max_result:
            return {}

        r = {}

        for token_id, token in self.level_state["players"][player_id][
            "tokens"].items():

            if token.get_pool() != get_pool("start"):
                continue

            r[token_id] = token

            # additional checks

            if self.is_token_at_destination(player_id, token_id):
                log_err("token at destination")

            if token.get_current_state() == self.default_start_state:
                continue
            else:
                log_err("not at def start state")
                log_err(f"{ token.get_pool()=} {token.get_current_state()=}")

            # skip if jumping over token in restricted area (pool 3)
            if not self.is_not_jumping_over_restricted(player_id=player_id,
                                                       token_id=token_id,
                                                       step=dice_result):
                log_err("1 jump")

        return r

    def state_exists(self, player_id, state):

        return state in self.level_state["players"][player_id]["states"]

    def get_from_board(self, player_id, dice_result):
        """
        select tokens
        from board

        filter player_id
        filter pool = live | safe

        filter current_state + dice_result in states

        return all tokens on board
        {token_id -> token}

        """

        r = {}

        for token_id, token in self.level_state["players"][player_id][
            "tokens"].items():

            # skip if at destination
            if self.is_token_at_destination(player_id, token_id):
                continue

            # check if in pools
            if not any(token.get_pool() == p for p in
                       [get_pool("live"), get_pool("safe")]):
                continue

            if not self.state_exists(player_id,
                                     token.get_current_state() + dice_result):
                continue

            # skip if jumping over token in restricted area (pool 3)
            if not self.is_not_jumping_over_restricted(player_id=player_id,
                                                       token_id=token_id,
                                                       step=dice_result):
                continue

            r[token_id] = token

        return r

    def is_token_at_destination(self, player_id, token_id):
        """wrapper"""

        # return False
        return self.level_state["players"][player_id]["tokens"][
            token_id].get_is_at_destination()

    def is_not_jumping_over_restricted(self, player_id, token_id, step):
        this_token = self.level_state["players"][player_id]["tokens"][token_id]

        this_restricted_states = get_destination_pool()[player_id]

        if not (
                this_token.get_current_state() + step in this_restricted_states):
            return True

        # in restricted
        occupied = []

        for t_id, t_meta in self.level_state["players"][player_id][
            "tokens"].items():

            if t_meta.get_pool() != get_pool("safe"):
                continue

            if t_id == token_id:
                continue

            if int(t_meta.get_current_state()) < int(
                    this_token.get_current_state()):
                continue

            if t_meta.get_current_state() in this_restricted_states:
                occupied.append(t_meta.get_current_state())

        if not occupied:
            return True

        lowest = min(occupied)

        return this_token.get_current_state() + step < lowest

    @staticmethod
    def is_at_destination(test_state, my_states, dest_states):
        if test_state not in dest_states:
            return False

        if set(my_states).issubset(set(dest_states)):
            return True

        dest_states.sort()
        this = False
        # from smaller to bigger
        for i in dest_states:
            # ignore prev to this
            if not this:

                if i == test_state:
                    this = True
                else:
                    continue

            if i not in my_states:
                return False

        return True

    def move_token(self, player_id, token_id, step):

        token = self.level_state["players"][player_id]["tokens"][token_id]

        if token.get_pool() == get_pool("start"):

            if step != 1:
                log_err("[err] integrity error: step must be 1")
                sys.exit(-1)

        this_states = self.level_state["players"][player_id]["states"]

        token.move_forward(
            step=step,
            states=this_states
        )

        token_count = self.level_state["players"][player_id]["tokens"].keys()

        keys = [i for i in this_states.keys()]
        last_n = []
        for _ in token_count:
            m = max(keys)
            keys.pop(m)
            last_n.append(m)

        my_tokens = []
        for t_id, t_meta in self.level_state["players"][player_id][
            "tokens"].items():
            my_tokens.append(t_meta.get_current_state())

        if self.is_at_destination(token.get_current_state(), my_tokens, last_n):
            token.set_at_destination()

        return {
            "eaten": self.check_eating(player_id, token_id),
            "is done": set(my_tokens).issubset(set(last_n))
        }

    def check_eating(self, player_id, token_id):

        token = self.level_state["players"][player_id]["tokens"][token_id]

        occupied = defaultdict(list)

        for p_id, p_meta in self.level_state["players"].items():

            for t_id, t in p_meta["tokens"].items():

                if t.get_pool() == get_pool("start"):
                    continue

                # skip those that are not on this tile
                if t.get_row_column() != token.get_row_column():
                    continue

                # skip this token
                if p_id == player_id and t_id == token_id:
                    continue

                occupied[p_id].append({
                    "token_id": t_id,
                    "token": t,
                    "player_id": p_id
                })

        if len(occupied) == 0:
            return []

        if len(occupied) != 1:
            log_err("err occupied eating")

        for owner, tokens in occupied.items():

            # i have my tokens here
            if owner == player_id:
                return []

            # one enemy token
            if len(tokens) == 1:
                for t in tokens:
                    t["token"].restart()

                return tokens

            # multiple enemy tokens, block rule
            elif len(tokens) > 1:
                token.restart()

                return [{
                    "token_id": token_id,
                    "player_id": player_id
                }]

        return []


class Token:

    def __init__(
            self,
            start_state,
            start_x_y,
    ):

        self.__start_state = start_state
        self.__start_x_y = start_x_y

        self.__current_state = start_state
        self.__current_x_y = start_x_y

        self.__is_at_destination = False

        self.__pool = get_pool("start")

    def get_current_state(self):
        return self.__current_state

    def get_row_column(self):
        return self.__current_x_y.row, self.__current_x_y.column

    def get_pool(self):
        return self.__pool

    def get_is_at_destination(self):
        if self.__pool != get_pool("safe") and self.__is_at_destination:
            log_err("err at destination, but not in safe pool")
        return self.__is_at_destination

    def set_at_destination(self):
        self.__is_at_destination = True

    def restart(self):

        if self.get_is_at_destination():
            log_err("token at destination")
            sys.exit(-1)

        self.__current_state = self.__start_state
        self.__current_x_y = self.__start_x_y
        self.__pool = get_pool("start")

    def _update_position(self, destination_state, states):

        self.__current_state = destination_state

        if self.__current_state not in states:
            log_err(f"trying to jump out of board {self.__current_state=}")

        self.__current_x_y = states[self.__current_state]
        self.__pool = self.__current_x_y.type

    def move_forward(self, step, states):
        """
        assumption:
            not used for moving token backwards (edge case where token is going
            back to start pool is not handled, in general moving pools back
             is not handled)

        detects:
            to big steps
            step <= 0
            token already at destination
            ...

        assumption: it is checked that this token is not jumping over other token
        in restricted jumping pool

        """

        if step <= 0:
            log_err(f"{step=}")

        if self.__is_at_destination:
            log_err('at destination, can not move')

        if not is_valid_pool(self.__pool):
            log_err(f"unknown pool {self.__pool}")

        if self.__pool == get_pool("start") and step != 1:
            log_err(f"step not 1 {step=}")

        if self.__pool == get_pool("start"):
            # todo dehardcode
            destination_state = 0

        else:
            destination_state = self.__current_state + step

        self._update_position(
            destination_state=destination_state,
            states=states
        )


class Level:

    def __init__(self, log=None):
        default_start_state = None
        default_start_tile = None

        game_conf = get_config()
        self.max_result = game_conf["dice number of sides"]

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

        playing_order = self.get_playing_order(game_conf)
        print(f"{playing_order=}")

        m_player_to_moves = player_moves_preprocessor()

        players = {}

        for player_id in range(get_config()["number of players"]):
            tokens = {}

            for token_id in range(get_config()['tokens per player']):
                tokens[token_id] = Token(
                    start_state=default_start_state,
                    start_x_y=default_start_tile,
                )

            players[player_id] = tokens

        self.board = Board(
            players=players,
            m_player_to_moves=m_player_to_moves,
            game_conf=game_conf,
            default_start_state=default_start_state
        )

        for i in self.log:
            if i["action"] == "move":
                print("move token")

                t = self.board.move_token(
                    player_id=i["player"],
                    token_id=i["token"],
                    step=i["dice_result"]
                )
                #

        # for user choosing
        self.players_turn = None
        self.start_pool_options  = {}
        self.non_start_pool_options = {}

        self.manual_driver(game_conf, playing_order)
        # self.auto_driver(game_conf, playing_order)

    def get_playing_order(self, game_conf) -> list:
        """
        return e.g. [0, 2, 1]
        """

        goes_list = []
        for i in self.log:
            if i["action"] == "goes":
                goes_list.append(i["player"])

                if len(goes_list) == game_conf['number of players']:
                    break

        return goes_list

    def manual_driver(
            self,
            game_conf,
            playing_order,
    ):
        already_won = set()

        c = 0
        while True:
            c += 1

            for player_id in playing_order:

                can_roll_again = True

                while can_roll_again:

                    if game_conf['number of players'] == len(already_won) + 1:
                        """
                        last player lost
                        no need to play with only him
                        """
                        print("1 lost, other won, game done")
                        return

                    roll_result = get_dice_result()

                    can_roll_again = roll_result == self.max_result

                    self.log.append(
                        construct_roll(player=player_id, roll=roll_result)
                    )

                    start_pool_movable = self.board.get_from_start_pool(
                        player_id=player_id, dice_result=roll_result)
                    board_movable = self.board.get_from_board(
                        player_id=player_id,
                        dice_result=roll_result)

                    # print(f"{start_pool_movable=}")
                    # print(f"{board_movable=}")

                    # to_choose = {**start_pool_movable, **board_movable}
                    # print(f"{to_choose=}")

                    if start_pool_movable or board_movable:
                        self.players_turn = player_id
                        self.start_pool_options = start_pool_movable
                        self.non_start_pool_options = board_movable
                        # self.players_options = to_choose

                        return

                    # if start_pool_movable and board_movable:
                    #
                    #     for token_id, token in start_pool_movable.items():
                    #
                    #         t = choose(self.board, self.log, player_id, 1,
                    #                    token_id)
                    #
                    #         if t["won"]:
                    #             already_won.add(player_id)
                    #
                    #         break
                    #
                    # elif start_pool_movable:
                    #
                    #     for token_id, token in start_pool_movable.items():
                    #         t = choose(self.board, self.log, player_id, 1,
                    #                    token_id)
                    #
                    #         if t["won"]:
                    #             already_won.add(player_id)
                    #         break
                    #
                    # elif board_movable:
                    #
                    #     for token_id, token in board_movable.items():
                    #
                    #         t = choose(self.board, self.log, player_id,
                    #                    roll_result,
                    #                    token_id)
                    #
                    #         if t["won"]:
                    #             already_won.add(player_id)
                    #         break




    def auto_driver(
            self,
            game_conf,
            playing_order,
    ):
        already_won = set()

        c = 0
        while True:
            c += 1

            for player_id in playing_order:

                can_roll_again = True

                while can_roll_again:

                    roll_result = get_dice_result()

                    can_roll_again = roll_result == self.max_result

                    self.log.append(
                        construct_roll(player=player_id, roll=roll_result)
                    )

                    start_pool_movable = self.board.get_from_start_pool(
                        player_id=player_id, dice_result=roll_result)
                    board_movable = self.board.get_from_board(
                        player_id=player_id,
                        dice_result=roll_result)

                    if start_pool_movable and board_movable:

                        for token_id, token in start_pool_movable.items():

                            t = choose(self.board, self.log, player_id,
                                       token_id)

                            if t["won"]:
                                already_won.add(player_id)

                            break

                    elif start_pool_movable:

                        for token_id, token in start_pool_movable.items():
                            t = choose(self.board, self.log, player_id,
                                       token_id)

                            if t["won"]:
                                already_won.add(player_id)
                            break

                    elif board_movable:

                        for token_id, token in board_movable.items():

                            t = choose(self.board, self.log, player_id,
                                       token_id)

                            if t["won"]:
                                already_won.add(player_id)
                            break

                    if game_conf['number of players'] == len(already_won) + 1:
                        """
                        last player lost
                        no need to play with only him
                        """

                        return

    def get_log(self):
        return self.log


def generate_start():
    level = Level()
    return level.get_log()


def choose(board, log, player_id,  token_id):
    """
    wrapper for moving token

    """

    last_log = log[-1]
    if last_log["action"] == "roll":
        pass
    else:
        print("errr")
        return

    roll_result = last_log["dice_result"]

    # if in start pool then 1

    token = board.level_state["players"][player_id]["tokens"][token_id]

    if token.get_pool() == get_pool("start"):
        roll_result = 1


    t = board.move_token(player_id=player_id, token_id=token_id,
                         step=roll_result)



    log.append(move_token(
        player=player_id,
        token=token_id,
        step=roll_result
    ))

    eaten = t["eaten"]
    for i in eaten:
        log.append(log_eat_token(
            player=i["player_id"],
            token=i["token_id"],
        ))

    gw = t["is done"]
    if gw:
        log.append(log_won(player=player_id))

    return {"won": gw}


def generate_whole_game():
    level = Level()
    return level.get_log()

def generate_as_much_as_you_can():
    # user creates level
    # order is determined

    level = Level()
    for i in level.get_log():
        print(i)

    ret_log = level.get_log()
    to_choose = {**level.start_pool_options, **level.non_start_pool_options}

    # user needs to make a choice

    last_log = level.get_log()[-1]
    if last_log["action"] == "roll":
        pass
    else:
        print("errr")
        return

    player = last_log['player']
    dice_result = last_log["dice_result"]


    for token_id,  token in to_choose.items():

        choose(level.board, level.get_log(), player,  token_id)

        break

    print()
    for i in level.get_log():
        print(i)
    print()

    # now again

    level = Level(log=level.get_log())

    for i in level.get_log():
        print(i)

    # user choice again

    last_log = level.get_log()[-1]
    if last_log["action"] == "roll":
        pass
    else:
        print("errr")
        return

    player = last_log['player']
    dice_result = last_log["dice_result"]

    to_choose = {**level.start_pool_options, **level.non_start_pool_options}

    for token_id,  token in to_choose.items():

        choose(level.board, level.get_log(), player,  token_id)

        break

    print()
    for i in level.get_log():
        print(i)
    print()


    return level.get_log()


def main():
    # log = generate_whole_game()
    # for i in log:
    #     print(i)

    log = generate_as_much_as_you_can()


    # self.players_turn = player_id
    # self.players_options = to_choose


if __name__ == '__main__':
    main()
