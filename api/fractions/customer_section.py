from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from ..models import Customer
from ..serializer import CustomerSerializer
import json


# ======================
# ===== Add Customer
# ======================
def AddCustomer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        name = data.get('name')
        company_name = data.get('company_name')
        address = data.get('address')
        mobile = data.get('mobile')

        customer = Customer.objects.create(name=name, address=address, company_name=company_name, mobile=mobile)
        customer.save()
        
        return JsonResponse({'message': 'Customer registered successfully.'}, status=201)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


# =======================
# ===== View Customer
# =======================
def ViewCustomer(request, pk):
    if pk > 0:
        query = Customer.objects.all().order_by('-id')
        limit = 10
        offset = (pk - 1) * limit
        number_of_pages = len(query)/limit
        if offset + limit > len(query):
            to_value = offset + (len(query) - offset)
        else:
            to_value = offset + limit

        filter_records = query[offset:to_value]
        if isinstance(number_of_pages, float):
            number_of_pages = int(number_of_pages) + 1
        
        serializer = CustomerSerializer(filter_records, many=True)
        return JsonResponse([{"total_page": number_of_pages}] + serializer.data, safe=False)


# =======================
# ===== Update Customer
# =======================
def UpdateCustomer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    serializer = CustomerSerializer(customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =======================
# ===== Delete Customer
# =======================
def DeleteCustomer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    try:
        customer.delete()
    except IntegrityError:
        return JsonResponse({'message': "Can't delete this Customer"}, status=201)

    return JsonResponse({'message': 'Removed customer from database.'}, status=201)
