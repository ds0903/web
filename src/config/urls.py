from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView  # noqa

from issues.api import IssuesAPI, IssuesRetriveAPI, back_issue, post_issues  # noqa
from users.api import UserCreateRetriveAPI, UserRetriveAPI, user_manager

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", IssuesAPI.as_view()),
    path("issues/post", post_issues),
    path("issues/<int:pk>", IssuesRetriveAPI.as_view()),
    path("auth/token/", TokenObtainPairView.as_view()),
    ###
    path("users/<int:pk>", UserRetriveAPI.as_view()),
    path("users/CLS", UserCreateRetriveAPI.as_view()),
    path("users/", user_manager),
]
