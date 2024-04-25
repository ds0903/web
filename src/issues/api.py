import json

# from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, serializers
# from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from issues.models import Issue
from permissions import IsADMIN
from users.enums import Role

from .enums import Status


class IssueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "title", "body"]


class IssueSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(required=False)
    junior = serializers.HiddenField(default=serializers.CurrentUserDefault())

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

    queryset = Issue.objects.all()


# @api_view()
# def retrive_issue(request, issue_id: int) -> Response:
#     instance = get_object_or_404(Issue, id=issue_id)

#     return Response(data={"result": IssueSerializer(instance).data})


# @api_view()
# def back_issue(request, issue_id: int) -> Response:
#     instance = get_object_or_404(Issue, id=issue_id)

#     return Response(data={"result": IssueSerializer(instance).data})
