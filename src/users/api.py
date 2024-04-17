import json

from django.contrib.auth import get_user_model
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User

# from rest_framework.response import Response


User = get_user_model()  # noqa


@csrf_exempt
def create_user(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        raise NotImplementedError("only POST request")

    data: dict = json.loads(request.body)
    user = User.objects.create_user(**data)  # noqa

    results = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "is_active": user.is_active,
    }
    return JsonResponse(results)
