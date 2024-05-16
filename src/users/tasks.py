import uuid

from django.core.mail import send_mail

from config.celery import celery_app


@celery_app.task
def send_activation_email(recipient: str, activation_link: uuid.UUID):
    send_mail(
        subject="User activation",
        message=f"Click on the link to activate your account: {activation_link}",  # noqa
        from_email="danil.grey15@gmail.com",
        recipient_list=[recipient],
    )


@celery_app.task
def send_confirm_email(user1: str, key: str):
    send_mail(
        subject="User activation done",
        message=f"Your account was activated by key: {key}",
        from_email="admin",
        recipient_list=[user1],
    )
