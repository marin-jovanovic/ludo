from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.game.resources import get_moves, \
    get_config, getMap, get_players, get_start_pool
from backend.api.view.comm import get_auth_ok_response_template


class BoardView(APIView):

    def get(self, request, name, resource):

        print("get board,", name, resource)
        response = get_auth_ok_response_template(request)

        configuration = {
            'startPool': get_start_pool,
            'moves': get_moves,
            'config': get_config,
            'map': getMap,
            # todo fetch from FE
            'players': get_players
        }

        response['payload'] = {
            "status": True,
            "payload": configuration[resource]()
        }

        return JsonResponse(response)


"""
lobby

    create room
        name


room
    create/:id

    get
       get all rooms
    
    put
        join
        leave
            
    
game
    
    get
        get all instructions
    
    make choice 
        move token
  
    get next instruction
    
statistics

    get/game
        
        get all statistics for this game
        
    


update game 
    notif all players that are in 
    


"""