from django.urls import path
from rest_framework import routers

from backend.api.view.login_view import LoginView
from backend.api.view.signup_view import SignUpView
from backend.api.view.logout_view import LogoutView
from backend.api.startup import startup_configuration
startup_configuration.print_app_logo()
from backend.api.view.validation_view import ValidationView
api_router = routers.DefaultRouter()

urlpatterns = [
    path("signup/<str:username>", SignUpView.as_view()),
    path("login/<str:username>", LoginView.as_view()),
    path("logout/<str:username>", LogoutView.as_view()),
    path("validate/<str:username>", ValidationView.as_view()),

    path("lobby/<str:username>", ValidationView.as_view()),

    # path("game/")
]
