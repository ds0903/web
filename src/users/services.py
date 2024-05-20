# import json
import uuid

# import redis
# from django.conf import settings

from shared.cache import CacheService

from .tasks import send_activation_email


class Activator:
    def __init__(self, email: str):
        self.email = email

    def create_activation_key(self) -> uuid.UUID:
        return uuid.uuid3(namespace=uuid.uuid4(), name=self.email)

    def create_activation_link(self, activation_key: uuid.UUID) -> str:
        return f"https://frontend.com/users/activate/{activation_key}"

    def send_user_activation_email(self, activation_key: uuid.UUID):
        # activation_key: uuid.UUID = create_activation_key(email)
        activation_link = self.create_activation_link(activation_key)

        send_activation_email.delay(
            recipient=self.email,
            activation_link=activation_link,
        )

    def save_activation_information(
        self, internal_user_id: int, activation_key: uuid.UUID
    ) -> None:
        cache = CacheService()
        payload = {"user_id": internal_user_id}
        cache.save(
            namespace="activation", key=activation_key, instance=payload, ttl=2_000
        )

        # print(internal_user_id, activation_key)
        # connection = redis.Redis.from_url(settings.CACHE_URL)

        # payload = {"user_id": internal_user_id}
        # connection.set(f"activation:{activation_key}", json.dumps(payload), ex=200)

        # raise NotImplementedError

    def validate_activation(self, activation_key: uuid.UUID) -> None:
        pass
