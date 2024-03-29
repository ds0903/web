import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from issues.models import Issue


@csrf_exempt
def post_issues(request) -> JsonResponse:
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
    return JsonResponse(data={"status": "allgood"})


def get_issues(request: HttpRequest) -> JsonResponse:
    issues = Issue.objects.all()

    result: list[dict] = [
        {
            "id": issue.id,
            "body": issue.body,
            "title": issue.title,
            "seni_id": issue.seni_id,
            "juni_id": issue.juni_id,
        }
        for issue in issues
    ]
    print("verygood")

    return JsonResponse(data={"results": result})
