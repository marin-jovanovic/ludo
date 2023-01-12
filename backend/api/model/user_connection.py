from django.apps import apps
from django.db import models

from backend.api.model.user import get_user_model_as_string


class UserConnection(models.Model):

    accepted = models.BooleanField(default=False)

    user_1 = models.ForeignKey(
        get_user_model_as_string(),
        on_delete=models.SET_NULL,
        null=True
    )
    user_2 = models.ForeignKey(
        get_user_model_as_string(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_requests_created'
    )


def get_user_connection_model():
    return apps.get_model("api.userConnection")
