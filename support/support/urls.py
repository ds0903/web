import httpx
import requests
from typing import Callable

from django.urls import path
from django.http import HttpRequest, HttpResponse, JsonResponse


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_current_market_state(request: HttpRequest) -> JsonResponse:
    source = request.POST.get("source")
    destination = request.POST.get("destination")
    key = "IQPS2UM7C0TZSC68"
    url = "https://www.alphavantage.co/query"

    params = {

        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": source,
        "to_currency": destination,
        "apikey": "demo",
    }

    response = requests.get(url, params=params)

    data = response.json()
    # rate = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    
    return JsonResponse(data)


        

    #http://localhost:8000/fetch-market?source=EUR&destination=USD
    #http://localhost:8000/fetch-market n\

def market(request: HttpRequest) -> HttpResponse:
    content="<h1>hi</h1>"
    return HttpResponse(content)

urlpatterns = [
    path(route="fetch-market", view=get_current_market_state),
    path(route="fetch", view=market),
]

#  """Response example:
#        {
#         "Realtime Currency Exchange Rate": {
#             "1. From_Currency Code": "UAH",
#             "2. From_Currency Name": "Ukrainian Hryvnia",
#             "3. To_Currency Code": "USD",
#             "4. To_Currency Name": "United States Dollar",
#             "5. Exchange Rate": "0.02610000",
#             "6. Last Refreshed": "2024-03-07 17:45:47",
#             "7. Time Zone": "UTC",
#             "8. Bid Price": "0.02609000",
#             "9. Ask Price": "0.02610000"
#         }
#     }
#     """