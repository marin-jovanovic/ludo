from backend.api.game.resources import get_moves, get_start_pool
from backend.api.game.tile import Tile


def get_start_pool_preprocessor():
    """
    player_id -> Tile
    """


    r = {}

    for player_id, tokens in get_start_pool().items():

        r[int(player_id)] = {}

        for token_id, tile in tokens.items():
            r[int(player_id)][int(token_id)] = Tile(tile["row"], tile["column"], tile["type"])

    return r


def player_moves_preprocessor():
    """
    state_id -> Tile

    """


    def aux(moves):

        r = {}

        for position, tile in moves.items():
            r[int(position)] = Tile(tile["row"], tile["column"], tile["type"])

        return r

    m_player_to_moves = get_non_start_states()


    # m_player_to_moves= get_moves()

    r = {}
    for player_id, moves in m_player_to_moves.items():
        r[player_id] = aux(moves)

    return r

def get_destination_pool():

    start_pool_enum = "3"

    reformated_states = get_non_start_states()

    # for p_id, states_meta in reformated_states.items():
    #     print(p_id, len(states_meta))
    #     for s_id, s_meta in states_meta.items():
    #         print(s_id, s_meta)

    r = {}

    for player_id, states in reformated_states.items():
        r[player_id] = {}

        for state_id, state_meta in states.items():
            if state_meta["type"] != start_pool_enum:
                continue

            r[player_id][state_id] = state_meta

    return r


def pre_states():
    start_pools = get_start_pool()

    for p_id, states_meta in start_pools.items():
        print(p_id, len(states_meta))
        for s_id, s_meta in states_meta.items():
            print(s_id, s_meta)

    print("---")
    return

    reformated_states = get_non_start_states()

    for p_id, states_meta in reformated_states.items():
        print(p_id, len(states_meta))
        for s_id, s_meta in states_meta.items():
            print(s_id, s_meta)


def get_non_start_states():
    start_state = "1"
    reformated_states = {}
    for player_id, states_meta in get_moves().items():

        reformated_states[player_id] = {}

        c = 0
        for s_id, s_meta in states_meta.items():

            if s_meta["type"] != start_state:
                reformated_states[player_id][c] = s_meta
                c += 1
    return reformated_states




if __name__ == '__main__':
    # for k,v in get_start_pool_preprocessor().items():
    #     print(k,v)

    pre_states()


