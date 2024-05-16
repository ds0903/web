import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, JsonResponse, response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, serializers
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from permissions import IsADMIN
from users.enums import Role

from .models import Activation, User
from .services import Activator
from .tasks import send_confirm_email

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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Получение сериализованных данных нового пользователя
        serialized_data = serializer.data

        # Теперь вы можете получить доступ к значениям полей, включая email
        email = serialized_data.get("email")

        activator_service = Activator(email)
        activation_key = activator_service.create_activation_key()

        Activation.objects.create(user=email, key=activation_key)

        activator_service.send_user_activation_email(
            activation_key=activation_key
        )  # noqa

        return Response(UserRegister(serializer.validated_data).data)


@api_view(["POST"])
def resend_activation_mail(request) -> response:
    key = request.data.get("key")
    try:
        activation1 = Activation.objects.get(key=key)
        user1 = activation1.user
        activation2 = User.objects.get(email=user1)
        activation2.is_active = True
        activation2.save()
        Activation.objects.filter(key=key).delete()
        send_confirm_email(user1, key)
        return Response(f"user: is updated: {user1}")

    except Activation.DoesNotExist:
        return Response(f"key dosnt exist: {key}")
