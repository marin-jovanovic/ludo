from django.apps import apps
from django.db import models

from backend.api.model.user import get_user_model


class ChatGroup(models.Model):
    # primary key
    # id

    # alternate primary key

    group_id = models.IntegerField()

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True
    )


def get_chat_group_model():
    return apps.get_model("api.chatgroup")
#
# def post_create_group():
#
#     creator = ""
#
#     participants = {
#         0: {
#             "userId": 0
#         },
#         1: {
#             "userId": 1
#         }
#     }
#
#     chat_group_model = get_chat_group_model()
#
#     r = chat_group_model(
#         user=creator
#     )
#     r.save()
