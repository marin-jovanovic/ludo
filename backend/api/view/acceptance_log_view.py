from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView

from backend.api.cqrs_c.acceptance_log import create_entry_if_not_exists, \
    check_all_accepted
from backend.api.cqrs_q.level_log import get_last_performed_by_all_users, \
    get_last_performed_by_this_user, get_any
from backend.api.model.user import get_user_model
from backend.api.view.comm import get_auth_ok_response_template

from backend.api.cqrs_c._cleanup import clean

class AcceptanceLogView(APIView):

    @transaction.atomic
    def get(self, request, level_id):

        clean(level_id)

        response = get_auth_ok_response_template(request)
        user_id = get_user_model().objects.get(username=request.username).id

        last_e_all = get_last_performed_by_all_users(level_id)
        last_e_this = get_last_performed_by_this_user(level_id=level_id,
                                                      user_id=user_id)
        last_e_any = get_any(level_id)

        response["payload"] = {
            "status": True,
            "lastExecutedByAll": last_e_all,
            "lastExecutedThisUser": last_e_this,
            "lastExecutedByAny": last_e_any
        }

        print(f"{last_e_all=}")
        print(f"{last_e_this=}")
        print(f"{last_e_any=}")
        return JsonResponse(response)

    # @transaction.non_atomic_requests
    @transaction.atomic
    def post(self, request, level_id, entry_id):
        """add new entry to log"""
        response = get_auth_ok_response_template(request)

        r = create_entry_if_not_exists(level_id, entry_id, request.username)
        if not r["status"]:
            return JsonResponse(response)

        response["payload"] = {
            "status": True
        }

        # transaction.on_commit(lambda: after_commit(entry_id, level_id, "transaction.on_commit"))

        # transaction.on_commit(lambda: some_celery_task.delay(my_object.pk))

        return JsonResponse(response)

def after_commit(entry_id, level_id, user_id):
    print("after commit")
    check_all_accepted(entry_id, level_id, user_id)

# @app.task
# def some_celery_task(object_pk)
#     my_object = MyObject.objects.get(pk=object_pk)