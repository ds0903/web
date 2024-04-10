import json

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from .models import User

User = get_user_model # noqa


@csrf_exempt
def create_user(request: HttpRequest) -> Response:
    if request.method != "POST":
        raise NotImplementedError("only POST request")

    data: dict = json.loads(request.body)
    user = User.objects.create(**data) # noqa
