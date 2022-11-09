from backend.api.game.resources import get_start_pool,_get_player_one_moves,_get_player_two_moves, _get_player_three_moves,_get_player_four_moves
from backend.api.game.tile import Tile


def get_start_pool_preprocessor():
    r = {}

    for player_id, tokens in get_start_pool().items():

        r[int(player_id)] = {}

        for token_id, tile in tokens.items():
            r[int(player_id)][int(token_id)] = Tile(tile["row"], tile["column"])

    return r


def player_moves_preprocessor():
    def aux(moves):

        r = {}

        for position, tile in moves.items():
            r[int(position)] = Tile(tile["row"], tile["column"])

        return r

    m_player_to_moves = {
        0: _get_player_one_moves(),
        1: _get_player_two_moves(),
        2: _get_player_three_moves(),
        3: _get_player_four_moves(),
    }

    r = {}
    for player_id, moves in m_player_to_moves.items():
        r[player_id] = aux(moves)

    return r
