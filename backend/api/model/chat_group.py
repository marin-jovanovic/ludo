import json

from django.apps import apps
from django.db import models

from backend.api.comm.comm import Notifier
from backend.api.model.level import get_level_model
from backend.api.model.level_log import get_level_log_model
from backend.api.model.user import get_user_model

class ChatGroup(models.Model):
    # primary key
    # id



    # alternate primary key

    # level = models.ForeignKey(
    #     get_level_model(),
    #     on_delete=models.SET_NULL,
    #     null=True
    # )
    #
    # log_entry = models.ForeignKey(
    #     get_level_log_model(),
    #     on_delete=models.SET_NULL,
    #     null=True
    # )
    #
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True
    )
    #
    # accepted = models.BooleanField(default=False)


def get_chat_group_model():
    return apps.get_model("api.chatgroup")

# def join_user()


def post_create_group():

    creator = ""

    participants = {
        0: {
            "userId": 0
        },
        1: {
            "userId": 1
        }
    }

    chat_group_model = get_chat_group_model()

    r = chat_group_model(
        user=creator
    )
    r.save()

