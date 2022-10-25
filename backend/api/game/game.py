import sys
from collections import defaultdict
from random import SystemRandom


def get_dice_result():
    crypto_generator_object = SystemRandom()
    return crypto_generator_object.randrange(
        get_config()['dice number of sides']) + 1


def get_player_one_moves():
    return {
        '-1': {
            "row": -1,
            "column": -1
        },
        "0": {
            "row": 6,
            "column": 1
        },
        "1": {
            "row": 6,
            "column": 2
        },
        "2": {
            "row": 6,
            "column": 3
        },
        "3": {
            "row": 6,
            "column": 4
        },
        "4": {
            "row": 6,
            "column": 5
        },
        "5": {
            "row": 5,
            "column": 6
        },
        "6": {
            "row": 4,
            "column": 6
        },
        "7": {
            "row": 3,
            "column": 6
        },
        "8": {
            "row": 2,
            "column": 6
        },
        "9": {
            "row": 1,
            "column": 6
        },
        "10": {
            "row": 0,
            "column": 6
        },
        "11": {
            "row": 0,
            "column": 7
        },
        "12": {
            "row": 0,
            "column": 8
        },
        "13": {
            "row": 2,
            "column": 8
        },
        "14": {
            "row": 3,
            "column": 8
        },
        "15": {
            "row": 4,
            "column": 8
        },
        "16": {
            "row": 5,
            "column": 8
        },
        "17": {
            "row": 6,
            "column": 9
        },
        "18": {
            "row": 6,
            "column": 10
        },
        "19": {
            "row": 6,
            "column": 11
        },
        "20": {
            "row": 6,
            "column": 12
        },
        "21": {
            "row": 6,
            "column": 13
        },
        "22": {
            "row": 6,
            "column": 14
        },
        "23": {
            "row": 7,
            "column": 14
        },
        "24": {
            "row": 8,
            "column": 14
        },
        "25": {
            "row": 8,
            "column": 12
        },
        "26": {
            "row": 8,
            "column": 11
        },
        "27": {
            "row": 8,
            "column": 10
        },
        "28": {
            "row": 8,
            "column": 9
        },
        "29": {
            "row": 9,
            "column": 8
        },
        "30": {
            "row": 10,
            "column": 8
        },
        "31": {
            "row": 11,
            "column": 8
        },
        "32": {
            "row": 12,
            "column": 8
        },
        "33": {
            "row": 13,
            "column": 8
        },
        "34": {
            "row": 14,
            "column": 8
        },
        "35": {
            "row": 14,
            "column": 7
        },
        "36": {
            "row": 14,
            "column": 6
        },
        "37": {
            "row": 12,
            "column": 6
        },
        "38": {
            "row": 11,
            "column": 6
        },
        "39": {
            "row": 10,
            "column": 6
        },
        "40": {
            "row": 9,
            "column": 6
        },
        "41": {
            "row": 8,
            "column": 5
        },
        "42": {
            "row": 8,
            "column": 4
        },
        "43": {
            "row": 8,
            "column": 3
        },
        "44": {
            "row": 8,
            "column": 2
        },
        "45": {
            "row": 8,
            "column": 1
        },
        "46": {
            "row": 8,
            "column": 0
        },
        "47": {
            "row": 7,
            "column": 0
        },
        "48": {
            "row": 7,
            "column": 1
        },
        "49": {
            "row": 7,
            "column": 2
        },
        "50": {
            "row": 7,
            "column": 3
        },
        "51": {
            "row": 7,
            "column": 4
        },
        "52": {
            "row": 7,
            "column": 5
        },
        "53": {
            "row": 7,
            "column": 6
        }
    }


def get_player_two_moves():
    return {
        '-1': {
            "row": -1,
            "column": -1
        },
        "0": {
            "row": 1,
            "column": 8
        },
        "1": {
            "row": 2,
            "column": 8
        },
        "2": {
            "row": 3,
            "column": 8
        },
        "3": {
            "row": 4,
            "column": 8
        },
        "4": {
            "row": 5,
            "column": 8
        },
        "5": {
            "row": 6,
            "column": 9
        },
        "6": {
            "row": 6,
            "column": 10
        },
        "7": {
            "row": 6,
            "column": 11
        },
        "8": {
            "row": 6,
            "column": 12
        },
        "9": {
            "row": 6,
            "column": 13
        },
        "10": {
            "row": 6,
            "column": 14
        },
        "11": {
            "row": 7,
            "column": 14
        },
        "12": {
            "row": 8,
            "column": 14
        },
        "13": {
            "row": 8,
            "column": 12
        },
        "14": {
            "row": 8,
            "column": 11
        },
        "15": {
            "row": 8,
            "column": 10
        },
        "16": {
            "row": 8,
            "column": 9
        },
        "17": {
            "row": 9,
            "column": 8
        },
        "18": {
            "row": 10,
            "column": 8
        },
        "19": {
            "row": 11,
            "column": 8
        },
        "20": {
            "row": 12,
            "column": 8
        },
        "21": {
            "row": 13,
            "column": 8
        },
        "22": {
            "row": 14,
            "column": 8
        },
        "23": {
            "row": 14,
            "column": 7
        },
        "24": {
            "row": 14,
            "column": 6
        },
        "25": {
            "row": 12,
            "column": 6
        },
        "26": {
            "row": 11,
            "column": 6
        },
        "27": {
            "row": 10,
            "column": 6
        },
        "28": {
            "row": 9,
            "column": 6
        },
        "29": {
            "row": 8,
            "column": 5
        },
        "30": {
            "row": 8,
            "column": 4
        },
        "31": {
            "row": 8,
            "column": 3
        },
        "32": {
            "row": 8,
            "column": 2
        },
        "33": {
            "row": 8,
            "column": 1
        },
        "34": {
            "row": 8,
            "column": 0
        },
        "35": {
            "row": 7,
            "column": 0
        },
        "36": {
            "row": 6,
            "column": 0
        },
        "37": {
            "row": 6,
            "column": 2
        },
        "38": {
            "row": 6,
            "column": 3
        },
        "39": {
            "row": 6,
            "column": 4
        },
        "40": {
            "row": 6,
            "column": 5
        },
        "41": {
            "row": 5,
            "column": 6
        },
        "42": {
            "row": 4,
            "column": 6
        },
        "43": {
            "row": 3,
            "column": 6
        },
        "44": {
            "row": 2,
            "column": 6
        },
        "45": {
            "row": 1,
            "column": 6
        },
        "46": {
            "row": 0,
            "column": 6
        },
        "47": {
            "row": 0,
            "column": 7
        },
        "48": {
            "row": 1,
            "column": 7
        },
        "49": {
            "row": 2,
            "column": 7
        },
        "50": {
            "row": 3,
            "column": 7
        },
        "51": {
            "row": 4,
            "column": 7
        },
        "52": {
            "row": 5,
            "column": 7
        },
        "53": {
            "row": 6,
            "column": 7
        }
    }


def get_config():
    return {
        "number of players": 4,
        "tokens per player": 4,
        "dice number of sides": 6,

        # assumption: talking for each player individually
        # if True: all tokens must reach the same destination
        # else: each token has it unique(multiple can go to same destination, but it is not a rule)
        # destination location
        "flag: same destination": True,

        # highest: highest goes first and then clockwise or anticlockwise (6, right, right, right)
        # order: 1st, 2nd, 3rd, 4th highest roll (6, 3, 2, 1)
        'choice: highest; order': True,

        # if highest then in which direction
        'choice: clockwise; anticlockwise': False,

        # when rolling dice to see who goes first
        # skip if tie will occur
        'flag: tie in order': False,

    }


class Tile:

    def __init__(self, row, column):
        self.row = row
        self.column = column

        # self.visitors = set()

    # def add_visitor(self, visitor):
    #     if visitor in self.visitors:
    #         print("visitor already in this")
    #         sys.exit(-1)
    #
    #     self.visitors.add(visitor)

    def __str__(self):
        return f"row: {self.row}, column: {self.column}"

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Tile):
            return self.row == other.row and self.column == other.column
        return False

        # def __eq__(self, other):
        #     if isinstance(other, self.__class__):
        #         return self.__dict__ == other.__dict__
        #     else:
        #         return False
        # return NotImplemented

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(tuple(sorted(self.__dict__.items())))


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


def determine_order(
        number_of_players, choice_highest_or_order,
        choice_clockwise_or_anticlockwise, f_tie_in_order):


    def construct_goes(player):
        return {
            "game": None,
            "player": player,
            "token": None,
            "dice_result": None,
            "action": "goes"
        }

    def construct_roll(player, roll):
        return {
            "game": None,
            "player": player,
            "token": None,
            "dice_result": roll,
            "action": "roll"
        }

    def construct_tie():
        return {
            "game": None,
            "player": None,
            "token": None,
            "dice_result": None,
            "action": "tie"
        }

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

                    roll_history.append(construct_goes(current_iteration_roll_history[0]['player']))

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


class Board:

    def __init__(self, row_count, column_count, players):
        self.row_count = row_count
        self.column_count = column_count
        self.players = players

        p = {
            1: get_player_one_moves(),
            2: get_player_two_moves(),
            3: get_player_one_moves()
        }
        self.universal_tiles_to_player_tiles_mapping = generate_tile_mapping(p)

        # for tile, tile_id in self.universal_tiles_to_player_tiles_mapping.items():
        #     print(tile, '=>', [str(i) for i in tile_id])

        self.board_state = defaultdict(lambda: defaultdict(set))
        for p_id, p in players.items():
            # print(p_id,p)
            for t_id, token in p.items():
                # print(str(token))
                token_global_position = token.normalize_position()
                row = token_global_position['row']
                column = token_global_position['column']
                self.board_state[row][column].add(token)

    def move_token(self, player, token_id, step):
        token = Token(id_=token_id, owner=player, destination_position=None,
                      moves=None)
        token_global_position = self.players[player][
            token_id].normalize_position()
        row = token_global_position['row']
        column = token_global_position['column']

        to_remove = None
        for token in self.board_state[row][column]:
            if token.id_ == token_id and token.owner == player:
                to_remove = token

        self.board_state[row][column].remove(to_remove)

        self.players[player][token_id].update_position(step)

        token_global_position = self.players[player][
            token_id].normalize_position()
        row = token_global_position['row']
        column = token_global_position['column']

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

        for row, m_c_to_tokens in self.board_state.items():
            for column, tokens in m_c_to_tokens.items():
                print(row, column, [str(i) for i in tokens])
        print()


class Player:

    def __init__(self, tokens):
        self.tokens = tokens


class Token:

    def __init__(self, id_, destination_position, owner, moves):
        self.id_ = id_
        self.position = -1
        self.destination_position = destination_position
        self.is_at_destination = False
        self.owner = owner
        self.moves = moves

    # def __eq__(self, other):
    #     """Overrides the default implementation"""
    #     if isinstance(other, Token):
    #         return self.id_ == other.id_ and self.owner == other.owner
    #     return False

    def normalize_position(self):
        return self.moves[str(self.position)]

    def update_position(self, step):
        if self.is_at_destination:
            print('at destination, can not move')
            return

        self.position += step
        if self.position >= self.destination_position:
            self.set_is_at_destination()

    def set_is_at_destination(self):
        self.is_at_destination = True

    def __str__(self):
        return f'{self.owner=}, {self.id_=}'


def alt():
    token_paths = {
        0: get_player_two_moves(),
        1: get_player_one_moves(),

    }

    token_one_path = None
    token_two_path = None


def board_configuration():
    def player_to_path_config():
        return {
            0: get_player_one_moves(),
            1: get_player_one_moves(),
            2: get_player_two_moves(),
            3: get_player_one_moves()
        }

    r = {}
    for i in range(get_config()['number of players']):
        t = {}
        for j in range(get_config()['tokens per player']):
            t[j] = player_to_path_config()[i]
        r[i] = t

    print('111111')
    print(r)

    # player id
    #     token id

    return {
        0: {
            0: player_to_path_config()[0],
            1: 'path1',
            2: 'path1',
            3: 'path1',
        },
        1: {
            0: 'path1',
            1: 'path1',
            2: 'path1',
            3: 'path1',
        },
    }


def main():
    # game_conf = get_config()
    #
    # order = determine_order(
    #     game_conf['number of players'],
    #     game_conf['choice: highest; order'],
    #     game_conf['choice: clockwise; anticlockwise'],
    #     game_conf['flag: tie in order'],
    # )
    #
    # print("log")
    # [print(i) for i in order]
    #
    # board_configuration()
    #
    # # f_same_destination = get_config()["flag: same destination"]
    # #
    # # if f_same_destination:
    # #     # print('same destination')
    # #     players_id = [i for i in range(get_config()['number of players'])]
    # #     # print(players_id)
    # #
    # #     # p = {i: for i in players_id}
    # #
    # # else:
    # #     # print('not same destination')
    # #     # print("not implemented")
    # #     sys.exit(-1)
    #
    # todo_destination_p = 500
    #
    # players = {}
    # for i in range(get_config()["number of players"]):
    #     tokens = {}
    #
    #     if i == 0:
    #         moves = get_player_one_moves()
    #     elif i == 1:
    #         moves = get_player_two_moves()
    #
    #     for j in range(get_config()['tokens per player']):
    #         tokens[j] = Token(j, destination_position=todo_destination_p, owner=i, moves=moves)
    #
    #     players[i] = tokens
    #
    # for k,v in players.items():
    #     print("player",k)
    #     for a,b in v.items():
    #         print("token", a,b)
    # # print(players)
    #
    # # players, tokens
    # b = Board(row_count=15, column_count=15, players=players)
    # #
    #
    # # move
    # print('move')
    # b.move_token(player=1, token_id=1, step=2)
    # order.append({"player": 1, "token": 1, "step": 2})
    # [print(i) for i in order]
    #
    # b.print_board_state()
    #
    # # move
    # print('move')
    # b.move_token(player=1, token_id=1, step=2)
    # b.print_board_state()
    #
    # # multiple at same location
    # print('multiple at the same location')
    # b.move_token(player=1, token_id=2, step=4)
    # b.print_board_state()
    #
    # print('move pl2')
    # b.move_token(player=2, token_id=1, step=3)
    # b.print_board_state()
    #
    # print('eat')
    # b.move_token(player=2, token_id=1, step=1)
    # b.print_board_state()

    print(80 * "-")
    order_driver()

    # roled = 6
    #
    # player_1_token_1 = Token(owner=1, current_tile=Tile(0, 0), destination_tile=None)


def order_driver():
    game_conf = get_config()

    order = determine_order(
        game_conf['number of players'],
        game_conf['choice: highest; order'],
        game_conf['choice: clockwise; anticlockwise'],
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
