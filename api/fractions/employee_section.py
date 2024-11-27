from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from ..models import Employee
from ..serializer import EmployeeSerializer
import json


# ======================
# ===== Add Employee
# ======================
def AddEmployee(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=201)

        name = data.get('name')
        address = data.get('address')
        nid_no = data.get('nid_no')
        mobile = data.get('mobile')
        # Check if nid exists or not
        check_nid = Employee.objects.filter(nid_no=nid_no).exists()
        if check_nid:
            return JsonResponse({'error': 'Nid already exists.'}, status=400)

        employee = Employee.objects.create(name=name, address=address, nid_no=nid_no, mobile=mobile)
        employee.save()
        
        return JsonResponse({'message': 'Employee registered successfully.'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


# =======================
# ===== View Employees
# =======================
def ViewEmployee(request, pk):
    if pk > 0:
        query = Employee.objects.all().order_by('-id')
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
        
        serializer = EmployeeSerializer(filter_records, many=True)
        return JsonResponse([{"total_page": number_of_pages}] + serializer.data, safe=False)


# =======================
# ===== Update Employees
# =======================
def UpdateEmployee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    serializer = EmployeeSerializer(employee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP)


# =======================
# ===== Delete Employees
# =======================
def DeleteEmployee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    try:
        employee.delete()
    except IntegrityError:
        return JsonResponse({'message': "Can't delete this Employee"}, status=201)
        
    return JsonResponse({'message': 'Removed employee from database.'}, status=201)
