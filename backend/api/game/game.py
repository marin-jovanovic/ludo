import sys
from collections import defaultdict

import backend.api.game.log
from backend.api.game.log import construct_roll, move_token
from backend.api.game.order import determine_order
from backend.api.game.pre import get_start_pool_preprocessor, \
    player_moves_preprocessor
from backend.api.game.resources import  get_config
from backend.api.game.tile import Tile


class TileVisitor:

    def __init__(self, player, players_tile_translation_id):
        self.player = player
        self.players_tile_translation_id = players_tile_translation_id

    def __str__(self):
        return f"player: {self.player}, tile: {self.players_tile_translation_id}"


# class Token:
#
#     def __init__(
#         self,
#         owner,
#         current_tile,
#         destination_tile
#     ):
#         self.owner = owner
#
#         self.current_tile = current_tile
#
#         self.destination_tile = destination_tile
#
#     def can_move(self):
#         return self.current_tile != self.destination_tile
#
#     def move(self, step):
#
#         print('move token')


class Board:

    def __init__(self,  players, start_pool):
        self.players = players

        self.start_pool = start_pool

        self.board_state = defaultdict(lambda: defaultdict(set))

        for p_id, p in self.players.items():
            for t_id, token in p.items():

                token_start_position = self.start_pool[p_id][token.id_]

                row = token_start_position.row
                column = token_start_position.column

                self.board_state[row][column].add(token)

    def has_any_on_board(self,player):
        for token_id, token in self.players[player].items():
            if not token.is_in_starting_pool:
                return True

    def get_from_start_pool(self, player):
        r = {}

        for token_id, token in self.players[player].items():
            if  token.is_in_starting_pool:
                r[token_id] = token
                # return True

        return r

    def get_from_board(self, player):
        r = {}

        for token_id, token in self.players[player].items():
            if not token.is_in_starting_pool:
                r[token_id] = token
                # return True

        return r

    def any_in_start_pool(self, player):

        for token_id, token in self.players[player].items():
            if token.is_in_starting_pool:
                return True

        # for token_id, tile in self.start_pool[player].items():
        #
        #     if self.board_state[tile.row][tile.column]:
        #         return True
        #
        # return False

    def move_token(self, player, token_id, step):

        # if self.players[player][
        #     token_id].is_in_starting_pool:
        #
        #     print("in starting pool")


        # print(f"{self.players[player]=}")

        token_global_position = self.players[player][
            token_id].normalize_position()

        # print(f"{token_global_position=}")

        row = token_global_position.row
        column = token_global_position.column

        # row = token_global_position['row']
        # column = token_global_position['column']

        # if self.players[player][
        #     token_id].is_in_starting_pool:
        #     print("in starting pool, no need to check")


        to_remove = set()
        for token in self.board_state[row][column]:
            if token.id_ == token_id and token.owner == player:
                to_remove.add(token)

        for i in to_remove:
            self.board_state[row][column].remove(i)


        self.players[player][token_id].update_position(step)

        token_global_position = self.players[player][
            token_id].normalize_position()

        row = token_global_position.row
        column = token_global_position.column
        # row = token_global_position['row']
        # column = token_global_position['column']

        if self.board_state[row][column]:
            # someone is here
            to_remove = set()

            for i in self.board_state[row][column]:
                if i.owner == player:
                    print('mine is already here')
                else:
                    print('someone else is here, perform eating')
                    to_remove.add(i)

            for i in to_remove:
                self.board_state[row][column].remove(i)

        self.board_state[row][column].add(self.players[player][token_id])

    def print_board_state(self):
        # print(f"{self.start_pool=}")

        # print("start pool")

        for row, m_c_to_tokens in self.board_state.items():
            for column, tokens in m_c_to_tokens.items():

                print(row, column, [str(i) for i in tokens])
        print()


class Player:

    def __init__(self, tokens):
        self.tokens = tokens



class Token:

    def __init__(self, start_tile,
 id_, destination_position, owner, moves):
        self.id_ = id_

        self.current_position = None
        self.current_tile = start_tile

        # todo logic when is in it

        # todo in starting pool there is only one place where token can be
        # token can not be placed in multiple places in starting pool
        self.is_in_starting_pool = True
        self.start_tile = start_tile

        # self.norm_row = None
        # self.norm_col = None

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
        # print(f"{self.moves=}")

        if self.is_in_starting_pool:
            return self.start_tile

        return self.moves[self.current_position]

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
            return

        self.current_position += step
        if self.current_position >= self.destination_position:
            self.set_is_at_destination()

    def set_is_at_destination(self):
        self.is_at_destination = True

    def __str__(self):
        return f'{self.owner=}, {self.id_=}'


    # board_configuration()

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

from backend.api.game.dice import get_dice_result


def main():
    log = []

    # get_player_one_moves_wrapper()
    # return

    # print(80 * "-")
    # order_driver()
    #
    game_conf = get_config()
    #
    order = determine_order(
        game_conf['number of players'],
        game_conf['choice: highest; order'],
        game_conf['choice: clockwise; anticlockwise'],
        game_conf['flag: tie in order'],
    )

    log += order

    print("log")
    [print(i) for i in log]
    print()


    goes_list = []
    number_of_players = game_conf['number of players']

    for i in log:
        if i["action"] == "goes":
            goes_list.append(i["player"])

            if len(goes_list) == number_of_players:
                break



    todo_destination_p = 500



    m_player_to_moves = player_moves_preprocessor()

    start_pool = get_start_pool_preprocessor()



    players = {}
    for player_id in range(get_config()["number of players"]):
        tokens = {}

        for token_id in range(get_config()['tokens per player']):

            start_tile = start_pool[player_id][token_id]

            tokens[token_id] = Token(
                owner=player_id,
                id_=token_id,

                start_tile=start_tile,

                destination_position=todo_destination_p,
                moves=m_player_to_moves[player_id]
            )

        players[player_id] = tokens

    b = Board(players=players, start_pool = start_pool)

    print("board state")
    b.print_board_state()

    print(f"{goes_list=}")
    print()

    max_result = 6

    for player_id in goes_list:
        print(f"player {player_id} move")
        # print(i)

        can_roll_again = True

        i = 0
        while can_roll_again:
            can_roll_again = False
            i += 1
            print("iteration", i)

            roll_result = get_dice_result()
            print(f"{roll_result=}")

            choose_count = 0
            move_from_start_pool = False
            move_on_board = False

            if roll_result == max_result:
                can_roll_again = True

            log.append(construct_roll(player=player_id, roll=roll_result))

            if roll_result == max_result and b.any_in_start_pool(player=player_id):
                choose_count += 1
                move_from_start_pool = True
                print("can move at least one from start pool")

            if b.has_any_on_board(player=player_id):
                choose_count += 1
                move_on_board = True
                print("can move at least one from board, todo one or multiple")

                roll_result = b.get_from_board(player=player_id)
                print(f"{roll_result=}")


            else:
                print("nothing to move from board")

            if choose_count == 0:
                print("no op, auto")
            elif choose_count == 1:
                print("auto")

                if move_from_start_pool:
                    sp = b.get_from_start_pool( player_id)
                    for token_id, token in sp.items():
                        print(token_id, token)

                        b.move_token(player=player_id, token_id=token_id, step=roll_result)

                        log.append(move_token(
                            player=player_id,
                            token=token_id,
                            step=roll_result
                        ))

                        break


                if move_on_board:
                    print("todo")
                    # get_from_board(self, player
                    # log.append()

            elif choose_count > 1:
                print("must choose")

                #     todo user input

            # if choose_count > 1:
            #     print("must choose")
            # elif choosable:
            #     print("automatic")
            print()


        # if can:
        #     # check if can choose
        #     log.append(choose(player_id))
        # else:
        #     print("perform action automatically")

        # if r == 6:
        #     print("can go")
        #
        #     can = b.any_in_start_pool(player=player_id)
        #
        #     if can:
        #         # check if can choose
        #         log.append(choose(player_id))
        #     else:
        #         print("perform action automatically")
        #
        # else:
        #
        #     # check if action can be done
        #     log.append(skip(player_id))

    print("log")
    [print(i) for i in log]
    print()

    print("return")
    return

    # print("----")

    # move
    print('move')


    backend.api.game.log.move_token(player=1, token_id=1, step=2)
    # order.append(move_token(None, 1, 1, 2))
    # [print(i) for i in order]

    b.print_board_state()

    # move
    print('move')
    backend.api.game.log.move_token(player=1, token_id=1, step=2)
    b.print_board_state()

    # multiple at same location
    print('multiple at the same location')
    backend.api.game.log.move_token(player=1, token_id=2, step=4)
    b.print_board_state()

    print('move pl2')
    backend.api.game.log.move_token(player=2, token_id=1, step=3)
    b.print_board_state()

    print('eat')
    backend.api.game.log.move_token(player=2, token_id=1, step=1)
    b.print_board_state()


    # roled = 6
    #
    # player_1_token_1 = Token(owner=1, current_tile=Tile(0, 0), destination_tile=None)


def order_driver():
    game_conf = get_config()

    order = determine_order(
        game_conf['number of players'],
        game_conf['choice: highest; order'],
        game_conf['choice: clockwise; anticlockwise'],
        # True
        game_conf['flag: tie in order'],
    )

    for i in order:
        print(i)

def generate_tile_mapping(p):
    m_tile_to_move = defaultdict(set)
    for player_id, moves in p.items():

        for tile_id, coordinates in moves.items():

            tile = Tile(**coordinates)

            tile_visitor = TileVisitor(player_id, tile_id)

            if tile_visitor in m_tile_to_move[tile]:
                print('add error')
                sys.exit(-1)

            m_tile_to_move[tile].add(tile_visitor)
    return m_tile_to_move


if __name__ == '__main__':
    main()


