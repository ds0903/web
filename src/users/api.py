import json

from django.contrib.auth import get_user_model
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, serializers

from .models import User

User = get_user_model()  # noqa


@csrf_exempt
def user_manager(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        raise NotImplementedError("only POST request!")
    if request.method == "POST":
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRetriveAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "delete"]
    serializer_class = UserSerializer
    queryset = User.objects.all()


# class UserCreateRetriveAPI(generics.ListCreateAPIView):

#     http_method_names = ["get", "post"]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
