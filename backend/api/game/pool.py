def pool_options():
    return {
        "start": "1",
        "live": "2",
        "safe": "3"
    }


def get_pool(type_):
    """
    vals are those from Fe generating board part
    """

    return pool_options()[type_]


def is_valid_pool(pool):
    t = pool_options()

    return any(pool == get_pool(i) for i in t.keys())
