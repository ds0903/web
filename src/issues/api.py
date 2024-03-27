from django.http import HttpRequest, JsonResponse
from issues.models import Issue
from django.views.decorators.csrf import csrf_exempt
import random


@csrf_exempt

def post_issues(request: HttpRequest) -> JsonResponse:
    a=random.randint(1,50)
    b=random.randint(1,50)
    Issue.objects.create(
        title=f"test{a}",
        body=f"test{b}",
        juni_id = 2,
        seni_id = 4,
    )
    


      # issue = Issue.objects.all()
      #issue1 = Issue.objects.first()
    # result = {
    #     "sho1": issue1.id,
    #     "sho2": issue1.body,
    #     "sho3": issue1.title,
    #     "sho2": issue1.seni_id,
    #     "sho1": issue1.juni_id,

    # }
    # result={
    #      "create/ok"
    # }
    # print("good")

    return JsonResponse(data={"status": "allgood"})




def get_issues(request: HttpRequest) -> JsonResponse:
    issues = Issue.objects.all()
       
    result: list[dict] = [{
        "sho1": issue.id,
        "sho2": issue.body,
        "sho3": issue.title,
        "sho4": issue.seni_id,
        "sho5": issue.juni_id,
        } for issue in issues
        ]
    print("verygood")

    return JsonResponse(data={"results": result})