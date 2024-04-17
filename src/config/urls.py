from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView  # noqa

from issues.api import (IssuesAPI, IssuesRetriveAPI, back_issue,  # noqa
                        post_issues)
from users.api import create_user

# from rest_framework_simplejwt.views import token_obtain_pair


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/post", create_user),
    # path("users/post", create_user),
    path("issues/", IssuesAPI.as_view()),
    path("issues/post", post_issues),
    path("issues/<int:pk>", IssuesRetriveAPI.as_view()),
    path("auth/token/", TokenObtainPairView.as_view()),
]
