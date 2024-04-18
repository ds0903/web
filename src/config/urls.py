from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView  # noqa

from issues.api import (IssuesAPI, IssuesRetriveAPI, back_issue,  # noqa
                        post_issues)
from users.api import UserRetriveAPI, user_manager  # UserCreateRetriveAPI

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", IssuesAPI.as_view()),
    path("issues/post", post_issues),
    path("issues/<int:pk>", IssuesRetriveAPI.as_view()),
    path("auth/token/", TokenObtainPairView.as_view()),
    ###
    path("users/<int:pk>", UserRetriveAPI.as_view()),
    # path("users/", UserCreateRetriveAPI.as_view()),
    path("users/", user_manager),
]
