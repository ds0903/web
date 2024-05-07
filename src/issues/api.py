import json

from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, response, serializers
from rest_framework.decorators import api_view  # permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from issues.models import Issue, Message
from permissions import IsADMIN
from users.enums import Role

from .enums import Status


class IssueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "title", "body"]


class MessageSrializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # noqa
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())  # noqa

    class Meta:
        model = Message
        fields = "__all__"

    def save(self):
        if user := self.validated_data.pop("user", None):
            self.validated_data["user_id"] = user.id
        if issue := self.validated_data.pop("issue", None):
            self.validated_data["issue_id"] = issue.id

        return super().save()


class IssueSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(required=False)
    junior = serializers.HiddenField(default=serializers.CurrentUserDefault())  # noqa

    class Meta:
        model = Issue
        fields = "__all__"

    def validate(self, attrs):
        request = self.context["request"]  # noqa
        attrs["status"] = Status.OPENED
        # attrs["junior"] = request.user
        return attrs


class IssuesAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    # queryset = Issue.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Issue.objects.all()
        elif user.role == "senior":
            return Issue.objects.exclude(senior_id=user.id)
        else:
            return Issue.objects.filter(junior_id=user.id)

    # noqa
    def post(self, request):  # noqa
        if request.user.role == Role.SENIOR:
            raise Exception("the role is senior")

        return super().post(request)


@csrf_exempt
def post_issues(request) -> Response:
    data = json.loads(request.body)
    id_s = data.get("id")
    body_s = data.get("body")
    title_s = data.get("title")  # s = "start point"
    seni_id_s = data.get("seni_id")
    juni_id_s = data.get("juni_id")

    Issue.objects.create(
        id=id_s,
        juni_id=juni_id_s,
        seni_id=seni_id_s,
        title=title_s,
        body=body_s,
    )
    return Response(data={"status": "allgood"})


class IssuesRetriveAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "delete"]
    permission_classes = [IsADMIN]
    serializer_class = IssueSerializer
    # lookup_url_kwarg = "id"
    queryset = Issue.objects.all()


@api_view(["GET", "POST"])
def messages_api_dispather(request: Request, issue_id: int) -> Response:
    if request.method == "GET":
        messages = Message.objects.filter(
            Q(
                issue__id=issue_id,
            )
            & (
                Q(
                    issue__senior=request.user,
                )
                | Q(
                    issue__junior=request.user,
                )
            )
        ).order_by("-timestamp")

        # messages = Message.objects.filter(
        #     issue__id=issue_id,
        #     issue__senior=request.user,
        # ) | Message.objects.filter(
        #     issue__id=issue_id,
        #     issue__junior=request.user,
        # ).order_by("timestamp")

        serializer = MessageSrializer(messages, many=True)
        # breakpoint()
        return response.Response(serializer.data)
    else:
        issue = Issue.objects.get(id=issue_id)
        payload = request.data | {"issue": issue.id}
        serializer = MessageSrializer(
            data=payload, context={"request": request}
        )  # noqa
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # breakpoint()
        return response.Response(serializer.validated_data)


@api_view(["PUT"])
def issues_close(request: Request, id: int):
    issue = Issue.objects.get(id=id)
    if request.user.role != Role.SENIOR:
        raise PermissionError("only for senior")
    if issue.status != Status.OPENED or issue.senior is None:
        raise ValidationError({"message": "the issue is not opened"}, code=422)  # noqa
    else:
        issue = Issue.objects.update(id=id, Status=Status.CLOSED)
        serializer = IssueSerializer(issue)

        return response.Response(serializer.data)


# class UserToIssue(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.user.role == Role.ADMIN:
#             return True
#         return False


@api_view(["PUT"])
# @permission_classes
def issues_take(request: Request, id: int):
    issue = Issue.objects.get(id=id)
    # breakpoint()
    if request.user.role != Role.SENIOR:
        raise PermissionError("only for senior")

    elif issue.status != Status.OPENED or issue.senior is not None:
        raise ValidationError({"message": "the issue is not opened"}, code=422)  # noqa

    else:
        issue.senior = request.user
        issue.status = Status.IN_PROGRESS
        issue.save()
        serializer = IssueSerializer(issue)
        return response.Response(serializer.data)


# @api_view()
# def retrive_issue(request, issue_id: int) -> Response:
#     instance = get_object_or_404(Issue, id=issue_id)

#     return Response(data={"result": IssueSerializer(instance).data})


# @api_view()
# def back_issue(request, issue_id: int) -> Response:
#     instance = get_object_or_404(Issue, id=issue_id)

#     return Response(data={"result": IssueSerializer(instance).data})
