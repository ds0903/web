from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView  # noqa

from issues.api import IssuesRetriveAPI  # , post_issues  # noqa
from issues.api import issues_take  # noqa
from issues.api import IssuesAPI, issues_close, messages_api_dispather
from users.api import (UserCreateRetriveAPI, UserRetriveAPI,  # noqa
                       user_manager)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", IssuesAPI.as_view()),
    # path("issues/post", post_issues),
    path("issues/<int:pk>", IssuesRetriveAPI.as_view()),
    path("auth/token/", TokenObtainPairView.as_view()),
    ###
    path("users/<int:pk>", UserRetriveAPI.as_view()),
    path("users/CLS", UserCreateRetriveAPI.as_view()),
    path("users/", user_manager),
    path("issues/<int:issue_id>/messages", messages_api_dispather),
    ###
    path("issues/<int:id>/close", issues_close),
    path("issues/<int:id>/take", issues_take),
]
