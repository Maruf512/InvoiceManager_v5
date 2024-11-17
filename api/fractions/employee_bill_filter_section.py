from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from ..models import Customer
from ..serializer import CustomerSerializer
import json




def EmployeeBillFilter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        
        
        return JsonResponse({'message': 'Filter data'}, status=201)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

