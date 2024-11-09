from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Catagory, Products, Employee, Production, Inventory, EmployeeBill, Customer, Challan, CashMemo
from .serializer import *
import json



# ====================== Employee Section =====================
# ======================
# ===== Add Employee
# ======================
@csrf_exempt
def add_employees(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=201)

        name = data.get('name')
        address = data.get('address')
        nid_no = data.get('nid_no')
        mobile = data.get('mobile')

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
def view_employees(request, pk):
    if pk > 0:
        query = Employee.objects.all()
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
@api_view(['PUT'])
def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    serializer = EmployeeSerializer(employee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP)


# =======================
# ===== Update Employees
# =======================
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return JsonResponse({'message': 'Removed employee from database.'}, status=201)



# ====================== Customer Section =====================
# ======================
# ===== Add Customer
# ======================
@csrf_exempt
def add_customer(request):
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
def view_all_customer(request, pk):
    if pk > 0:
        query = Customer.objects.all()
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
@api_view(['PUT'])
def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    serializer = CustomerSerializer(customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# =======================
# ===== Delete Customer
# =======================
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return JsonResponse({'message': 'Removed customer from database.'}, status=201)



# ====================== Catagory Section =====================
# ======================
# ===== Add Catagory
# ======================
@csrf_exempt
def add_catagory(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        name = data.get('name')
        catagory = Catagory.objects.create(name=name)
        catagory.save()
        
        return JsonResponse({'message': 'Catagory registered successfully.'}, status=201)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)



# ======================
# ===== View Catagory
# ======================
def view_catagory(request):
    catagory = Catagory.objects.all()
    serializer = CatagorySerializer(catagory, many=True)
    return JsonResponse(serializer.data, safe=False)



# =======================
# ===== Delete Catagory
# =======================
def delete_catagory(request, pk):
    catagory = get_object_or_404(Catagory, pk=pk)
    catagory.delete()
    return JsonResponse({'message': 'Removed Catagory from database.'}, status=201)



# ====================== Products Section =====================
# =======================
# ===== Add Products
# =======================
@csrf_exempt
def add_products(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        name = data.get('name')
        rate = data.get('rate')
        catagory_id = data.get('catagory_id')

        products = Products.objects.create(name=name, rate=rate, catagory_id=catagory_id)
        products.save()
        
        return JsonResponse({'message': 'Products added successfully.'}, status=201)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)



# =======================
# ===== View Products
# =======================
def view_all_products(request, pk):
    data = []
    if pk > 0:
        query = Products.objects.all()
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
        
        for i in filter_records:
            catagory_name = get_object_or_404(Catagory, pk=i.catagory_id)
            data.append({'id': i.id, 'name': i.name, 'rate': i.rate, 'catagory_name':catagory_name.name})

        return JsonResponse([{"total_page": number_of_pages}] + data, safe=False)



# =======================
# ===== Update Products
# =======================
@api_view(['PUT'])
def update_products(request, pk):
    products = get_object_or_404(Products, pk=pk)
    serializer = ProductsSerializer(products, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# =======================
# ===== Delete Products
# =======================
def delete_products(request, pk):
    products = get_object_or_404(Products, pk=pk)
    products.delete()
    return JsonResponse({'message': 'Removed Products from database.'}, status=201)



# ====================== Production Section =====================
# =======================
# ===== Add Production
# =======================
@csrf_exempt
def add_production(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        products_id = data.get('products_id')
        employee_id = data.get('employee_id')
        quantity = data.get('quantity')
        rate = data.get('rate')

        production = Production.objects.create(products_id=products_id, employee_id=employee_id, quantity=quantity, rate=rate)
        production.save()
        
        return JsonResponse({'message': 'Production added successfully.'}, status=201)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)




# =======================
# ===== View Production
# =======================
def view_all_production(request, pk):
    data = []
    if pk > 0:
        query = Production.objects.all()
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
        
        for i in filter_records:
            products = get_object_or_404(Products, pk=i.products_id)
            employee = get_object_or_404(Employee, pk=i.employee_id)
            data.append({'id': i.id, 'products':f"{products.name}({i.products_id})", "employee":f"{employee.name}({i.employee_id})", "quantity":i.quantity, 'rate': i.rate})

        return JsonResponse([{"total_page": number_of_pages}] + data, safe=False)