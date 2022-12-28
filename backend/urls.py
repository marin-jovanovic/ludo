from django.urls import path
from rest_framework import routers

from backend.api.startup import startup_configuration
from backend.api.view.board_view import BoardView
from backend.api.view.game_view import GameView
from backend.api.view.lobby_view import LobbyView
from backend.api.view.login_view import LoginView
from backend.api.view.logout_view import LogoutView
from backend.api.view.message_view import MessageView
from backend.api.view.settings_view import SettingsView
from backend.api.view.signup_view import SignUpView
from backend.api.view.delete_profile_view import DeleteProfileView

startup_configuration.print_app_logo()
api_router = routers.DefaultRouter()

urlpatterns = [
    path("signup/<str:username>", SignUpView.as_view()),
    path("login/<str:username>", LoginView.as_view()),
    path("logout/<str:username>", LogoutView.as_view()),
    path("deleteProfile/<str:username>", DeleteProfileView.as_view()),

    # CRUD meta game
    path("lobby/", LobbyView.as_view()),
    path("lobby/<str:name>", LobbyView.as_view()),

    #
    path("game/", GameView.as_view()),
    path("game/<str:name>", GameView.as_view()),

    path("board/<str:name>/<str:resource>", BoardView.as_view()),

    path("message/", MessageView.as_view()),
    path("message/<str:game>", MessageView.as_view()),

    path("settings/", SettingsView.as_view()),


]
