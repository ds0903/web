import uuid

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
        pass

    def validate_activation(self, activation_key: uuid.UUID) -> None:
        pass
