from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView  # noqa
# from rest_framework_simplejwt.views import token_obtain_pair

from issues.api import get_issues, post_issues
from users.api import create_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/post", create_user),
    # path("users/post", create_user),
    path("issues/", get_issues),
    path("issues/post", post_issues),
    path("auth/token/", TokenObtainPairView.as_view()),
]
