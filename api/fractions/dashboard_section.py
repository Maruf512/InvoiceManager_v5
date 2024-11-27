from django.http import JsonResponse
from ..models import *


def ViewDashboard(request):
    return JsonResponse({'message': "loaded"}, safe=False, status=200)




