from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ["user_permission", "groups"]
    readonly_fields = [
        "password",
        "date_joined",
        "last_login",
        "is_superuser",
        # "is_active",
        # "is_staff",
        "email",
    ]
