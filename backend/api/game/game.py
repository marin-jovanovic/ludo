import sys
from collections import defaultdict

from backend.api.game.dice import get_dice_result
from backend.api.game.log import construct_roll, move_token, log_won, log_eat_token
from backend.api.game.order import determine_order
from backend.api.game.pre import get_start_pool_preprocessor, \
    player_moves_preprocessor
from backend.api.game.resources import get_config
from backend.api.game.pre import  get_destination_pool

# todo if user gets 5 but there are only 3 spaces left then move
#   do not wait till user gets 3 (for placing token in win position)
todo_move_to_last_if_exceed = True

default_start_state = None
default_start_tile = None
# done
# action eat
# if in end pool can not be eaten
# move max to destination, not over
# jump one by one

# todo check if jumping over can be made in restricted or they just have to be one after another

# fixme eating?

def log_err(content):
    print(content)

class Board:

    def __init__(self, players, m_player_to_moves):

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

        self.players = self.level_state["players"]

        self.max_result = 6

    def get_from_start_pool(self, player_id, dice_result):
        """
        return dict {token_id -> token}
        assumption: moving by 1 if in start pool, will not jump out of board
        """

        if dice_result != self.max_result:
            return {}

        r = {}

        for token_id, token in self.players[player_id]["tokens"].items():

            # check if in pools
            if token.get_pool() == get_pool("start"):
                r[token_id] = token

            else:
                continue

            # skip if at destination
            if self.is_token_at_destination(player_id, token_id):
                log_err("err 1 dest")

            if token.current_state == default_start_state:
                continue
            else:
                log_err("err not at def start state")
                log_err(f"{token.get_pool()=} {token.current_state=}")

            # skip if jumping over token in restricted area (pool 3)
            if not self.is_not_jumping_over_restricted(player_id=player_id, token_id=token_id, step=dice_result):
                log_err("err 1 jump")

        return r

    def state_exists(self, player_id, state):

        return state  in self.level_state["players"][player_id]["states"]

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

        for token_id, token in self.players[player_id]["tokens"].items():

            # skip if at destination
            if self.is_token_at_destination(player_id, token_id):
                continue

            # check if in pools
            if not any(token.get_pool() == p for p in [get_pool("live"),   get_pool("safe")]):
                continue



            if not self.state_exists(player_id, token.current_state + dice_result):
                continue

            # skip if jumping over token in restricted area (pool 3)
            if not self.is_not_jumping_over_restricted(player_id=player_id, token_id=token_id, step=dice_result):
                print("jumping over rest")
                continue

            r[token_id] = token

        return r

    def is_token_at_destination(self, player_id, token_id):
        """wrapper"""
        return self.players[player_id]["tokens"][token_id].get_is_at_destination()

    def get_winning_order(self):
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

    def is_not_jumping_over_restricted(self, player_id, token_id, step):
        this_token = self.players[player_id]["tokens"][token_id]

        this_restricted_states = get_destination_pool()[player_id]

        if not (this_token.current_state + step in this_restricted_states):
            return True

        # in restricted
        occupied = []

        for t_id, t_meta in self.players[player_id]["tokens"].items():

            if t_id == token_id:
                continue

            if t_meta.current_state in this_restricted_states:
                occupied.append(t_meta.current_state)

        if not occupied:
            return True

        lowest = min(occupied)

        return this_token.current_state + step < lowest

    def move_token(self, player_id, token_id, step):

        token = self.players[player_id]["tokens"][token_id]

        if token.get_pool() == get_pool("start"):

            if step != 1:
                log_err("[err] integrity error: step must be 1")
                sys.exit(-1)

        this_states = self.level_state["players"][player_id]["states"]

        is_moved = self.players[player_id]["tokens"][token_id].move_forward(
            step=step,
            states=this_states
        )

        if not is_moved:
            log_err(f"[err] can not move {player_id=} {token_id=}")

         # todo set flags for token, chech that

        return {
            # "player": player_id,
            "eaten": self.check_eating(player_id, token_id),
            "won order": self.get_winning_order()
        }

    def check_eating(self, player_id, token_id):

        token = self.players[player_id]["tokens"][token_id]

        occupied = defaultdict(list)

        for p_id, p_meta in self.players.items():

            for t_id, t in p_meta["tokens"].items():

                if t.get_pool() ==  get_pool("start"):
                    continue


                # skip those that are not on this tile
                if t.get_row_column() != token.get_row_column():
                    continue

                # skip this token
                if p_id  == player_id and t_id == token_id:
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

            # print()
            # print(player_id, token_id,token.get_row_column())
            # for p_id, p_meta in self.players.items():
            #     for t_id, t in p_meta["tokens"].items():
            #         print(p_id, t_id, t.get_row_column())

            # one enemy token
            if len(tokens) == 1:
                for t in tokens:
                    print("eat enemy")
                    t["token"].restart()

                return tokens

            # multiple enemy tokens, block rule
            elif len(tokens) > 1:
                print("eat me")
                token.restart()

                return [{
                    "token_id": token_id,
                    "player_id": player_id
                }]

        return []


def get_pool(type_):
    """
    vals are those from Fe generating board part
    """


    return {
        "start": "1",
        "live": "2",
        "safe": "3"
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
        return self.current_x_y.row, self.current_x_y.column

    def set_at_destination(self):
        self.is_at_destination = True

    def get_is_at_destination(self):
        if self.pool != get_pool("safe") and self.is_at_destination:
            log_err("err at destination, but not in safe pool")
        return self.is_at_destination

    def get_pool(self):
        return self.pool

    def restart(self):

        if self.get_is_at_destination():
            log_err("[err] token at destination")
            sys.exit(-1)

        self.current_state = self.start_state
        self.current_x_y = self.start_x_y
        self.pool = get_pool("start")

    def move_forward(self, step, states):
        """
        if step is to big, exception will be thrown, no need to check now

        assumption: it is checked that this token is not jumping over other token
        in restricted jumping pool

        this ensures that it can only go to his destination position

        """

        if step <= 0:
            log_err("[err] step 0")
            sys.exit(-1)

        if self.is_at_destination:
            log_err('[err] at destination, can not move')
            sys.exit(-1)

        if self.pool == get_pool("start"):
            if step != 1:
                log_err(f"err step not 1 {step=}")

            # todo dehardcode
            self.current_state = 0

        elif self.pool == get_pool("live"):

            if self.current_state + step not in states:
                log_err("[err] trying to jump out of board")

            self.current_state += step

        elif self.pool == get_pool("safe"):

            self.current_state += step

        else:
            log_err("[err] unknown pool")
            return False

        try:
            self.current_x_y = states[self.current_state]

        except KeyError:
            log_err("[err] trying to jump out of board")
            return False

        self.pool = self.current_x_y.type

        # how is jumping over restricted controlled?

        if max(states.keys()) == self.current_state:
            self.set_at_destination()
            print("at destination")


        return True


class Level:

    def __init__(self, log=None):
        game_conf = get_config()
        self.max_result = 6

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

        player_order = self.goes_list_driver(game_conf)

        m_player_to_moves = player_moves_preprocessor()

        # start_pool = get_start_pool_preprocessor()

        players = {}

        # was -1


        for player_id in range(get_config()["number of players"]):
            tokens = {}

            for token_id in range(get_config()['tokens per player']):
                # default_start_tile = start_pool[player_id][token_id]

                tokens[token_id] = Token(
                    start_state=default_start_state,
                    start_x_y=default_start_tile,
                )

            players[player_id] = tokens

        already_won = []
        self.board = Board(players=players, m_player_to_moves = m_player_to_moves)

        # todo manual

        self.auto_driver(already_won,  game_conf, player_order)

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


    def auto_driver(
        self,
            already_won,
            game_conf,
            goes_list,
    ):


        ttl = 500


        while True:

            ttl -= 1
            if ttl < 0:
                break

            for player_id in goes_list:

                can_roll_again = True

                while can_roll_again:

                    roll_result = get_dice_result()

                    can_roll_again = roll_result == self.max_result

                    self.log.append(
                        construct_roll(player=player_id, roll=roll_result)
                    )

                    start_pool_movable = self.board.get_from_start_pool(player_id=player_id, dice_result=roll_result)
                    board_movable = self.board.get_from_board(
                            player_id=player_id,
                            dice_result=roll_result)

                    if start_pool_movable and board_movable:

                        # to_choose = {**start_pool_movable, **board_movable}

                        for token_id, token in start_pool_movable.items():

                            # todo if from board_movable then this is not changed
                            t = choose(self.board, self.log, player_id, 1, token_id,
                                       already_won)

                            for j in t["won"]:
                                already_won.append(j)
                            break

                    elif start_pool_movable:

                        for token_id, token in start_pool_movable.items():
                            t = choose(self.board, self.log, player_id, 1, token_id,
                                       already_won)

                            for j in t["won"]:
                                already_won.append(j)
                            break

                    elif board_movable:

                        for token_id, token in board_movable.items():

                            t = choose(self.board, self.log, player_id, roll_result,
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

    log.append(move_token(
        player=player_id,
        token=token_id,
        step=roll_result
    ))

    eaten = t["eaten"]
    for i in eaten:
        print(i)
        log.append(log_eat_token(
            player=i["player_id"],
            token=i["token_id"],
        ))

    gw = t["won order"]
    for i in gw:
        if i not in already_won:
            log.append(log_won(player=i))

    return {"won": gw}


def generate_whole_game():
    level = Level()
    return level.get_log()


def main():
    log = generate_whole_game()

    print(len(log))

    for i, instr in enumerate(log[:100]):
        print(i, instr)

    #     nije napravljeno predprocesiranja stateova

    # print()
    # print()
    # print()
    # print()
    # cl = defaultdict(int)
    # for i, instr in enumerate(log[:100]):
    #
    #     if instr["action"] in ["move", "eaten"]:
    #         print(i, instr)
    #
    #     if instr["action"] == "move":
    #         cl[f"{instr['player']}{instr['token']}"] += instr["dice_result"]
    #         print(cl)

if __name__ == '__main__':
    main()
