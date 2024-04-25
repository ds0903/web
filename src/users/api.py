import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, serializers
from rest_framework.exceptions import ValidationError

from permissions import IsADMIN
from users.enums import Role

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
    permission_classes = [IsADMIN]
    http_method_names = ["get", "put", "delete"]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRegister(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "role"]

    def validate_role(self, value: str) -> str:
        if value not in Role.users():
            raise ValidationError(
                f"Selected Role must be in {Role.users_values()}"
            )  # noqa
        return value

    def validate(self, attrs: dict) -> dict:
        attrs["password"] = make_password(attrs["password"])

        return attrs


class UserCreateRetriveAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = UserRegister
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
