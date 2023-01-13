from django.urls import path
from rest_framework import routers

from backend.api.startup import startup_configuration
# from backend.api.view.game_view import GameView
from backend.api.view.acceptance_log_view import AcceptanceLogView
from backend.api.view.board_view import BoardView
from backend.api.view.delete_profile_view import DeleteProfileView
from backend.api.view.level_log_view import LevelLogView
from backend.api.view.level_view import LevelView
from backend.api.view.login_view import LoginView
from backend.api.view.logout_view import LogoutView
from backend.api.view.message_view import MessageView
from backend.api.view.settings_view import SettingsView
from backend.api.view.signup_view import SignUpView
from backend.api.view.user_view import UserView
from backend.api.view.music_view import MusicView
from backend.api.view.user_connection_view import UserConnectionView
from backend.api.view.user_page_view import UserPageView
from backend.api.view.user_profile_photo import UserProfilePhotoView
from backend.api.view.user_connection_request_view import UserConnectionRequestView
from backend.api.view.direct_message_view import DirectMessageView
startup_configuration.print_app_logo()
api_router = routers.DefaultRouter()

urlpatterns = [
    path("signup/<str:username>", SignUpView.as_view()),
    path("login/<str:username>", LoginView.as_view()),
    path("logout/<str:username>", LogoutView.as_view()),
    path("deleteProfile/<str:username>", DeleteProfileView.as_view()),

    # CRUD meta game
    path("level/", LevelView.as_view()),

    # todo actually this is level_name for post method
    path("level/<str:level_id>", LevelView.as_view()),
    # path("level/<str:level_id>", LevelView.as_view()),
    path("level/<str:level_id>/log", LevelLogView.as_view()),

    path("message/", MessageView.as_view()),
    path("message/<str:level_id>", MessageView.as_view()),

    path("settings/", SettingsView.as_view()),
    path("settings/<str:resource_id>", SettingsView.as_view()),

    path("music/", MusicView.as_view()),

    path("user/page/<str:page_id>", UserPageView.as_view()),
    path("user/profilePhoto/<str:user_id>", UserProfilePhotoView.as_view()),
    # path("user/connection", UserConnectionView.as_view()),

    # user_id
    path("directMessage/<str:user_id>", DirectMessageView.as_view()),
    path("user/connection", UserConnectionView.as_view()),
    path("user/connection/requests", UserConnectionRequestView.as_view()),
    path("user/connection/<str:user_id>", UserConnectionView.as_view()),
    path("user/connection/<str:connection_id>", UserConnectionView.as_view()),
    path("user/", UserView.as_view()),
    path("user/<str:user_id>", UserView.as_view()),

    path("level/<str:level_id>/acceptanceLog", AcceptanceLogView.as_view()),
    path("level/<str:level_id>/acceptanceLog/<str:entry_id>",
         AcceptanceLogView.as_view()),

    # todo fix this
    path("board/<str:level_id>", BoardView.as_view()),


    #
    # path("game/", GameView.as_view()),
    # path("game/<str:name>", GameView.as_view()),

]
