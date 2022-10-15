from django.urls import path
from rest_framework import routers

from backend.api.view.loginView import LoginView
from backend.api.view.signUpView import SignUpView

from backend.api.startup import startup_configuration
startup_configuration.print_app_logo()

api_router = routers.DefaultRouter()

urlpatterns = [
    path("signup/<str:username>", SignUpView.as_view()),
    path("login/<str:username>", LoginView.as_view()),

]
