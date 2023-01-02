#
# def is_any_entry_present(game):
#     r = __get_game(game)
#     if r["status"]:
#         game_o = r["payload"]
#     else:
#         return r
#     try:
#         any_entries = GameLog.objects.filter(game=game_o)
#
#         if bool(any_entries):
#             return {"status": True, "payload": True}
#         else:
#             return {"status": True, "payload": False}
#
#         # print(f"{any_entries=}")
#
#         # print(bool(any_entries), )
#
#         # .exists()
#     except GameLog.DoesNotExist:
#         return {"status": True, "payload": False}
#         # any_entries = None
#
#     # print(f"{any_entries=}")
#

# def __is_game_full(game_name):
#     r = __get_game(game_name)
#     if r["status"]:
#         game_o = r["payload"]
#     else:
#         return r
#
#     capacity = game_o.capacity
#
#     r = get_users_in_level(game_name)
#     if r["status"]:
#         currently_active_players = len(r["payload"])
#     else:
#         return r
#
#     return {"status": True, "payload": capacity <= currently_active_players}


# def __delete_game(name):
#     if __check_game_name_exists(name):
#         return {
#             "status": True,
#             "payload": get_level_model().objects.filter(name=name).delete()
#         }
#
#     return {"status": False}




# def __get_game(game_name):
#     try:
#         return {"status": True,
#                 "payload":
#                     _get_game_model().objects.get(name=game_name)}
#     except _get_game_model().DoesNotExist:
#         return {"status": False, "payload": "game not exist"}


# def __is_empty(game_name):
#     r = __get_game(game_name)
#     if r["status"]:
#         game_o = r["payload"]
#     else:
#         return r
#
#     r = len(
#         get_user_model().objects.filter(currently_playing=game_o)
#     )
#
#     return {"status": True, "payload": not r}


# def __free_user_currently_playing(username):
#     return __driver_assign_user_currently_playing(username, None)
#
#
# def __assign_user_currently_playing(username, game_name):
#     r = __get_game(game_name)
#     if r["status"]:
#         game_o = r["payload"]
#     else:
#         return r
#
#     return __driver_assign_user_currently_playing(username, game_o)
#
#
# def __driver_assign_user_currently_playing(username, status):
#     r = get_user(username)
#     if r["status"]:
#         user_o = r["payload"]
#     else:
#         return r
#
#     user_o.currently_playing = status
#     user_o.save()
#
#     return {"status": True}


