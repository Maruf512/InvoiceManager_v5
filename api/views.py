from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse, Http404
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Employee, Production, Inventory, EmployeeBill, Customer, Challan, CashMemo
from .serializer import *
import json
from math import ceil


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
# ===== Delete Employees
# =======================
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    try:
        employee.delete()
    except IntegrityError:
        return JsonResponse({'message': "Can't delete this Employee"}, status=201)
        
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
    try:
        customer.delete()
    except IntegrityError:
        return JsonResponse({'message': "Can't delete this Customer"}, status=201)

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
        catagory = Category.objects.create(name=name)
        catagory.save()
        
        return JsonResponse({'message': 'Catagory registered successfully.'}, status=201)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

# ======================
# ===== View Catagory
# ======================
def view_catagory(request):
    catagory = Category.objects.all()
    serializer = CatagorySerializer(catagory, many=True)
    return JsonResponse(serializer.data, safe=False)

# =======================
# ===== Delete Catagory
# =======================
def delete_catagory(request, pk):
    catagory = get_object_or_404(Category, pk=pk)
    try:
        catagory.delete()
    except IntegrityError:
        return JsonResponse({'message': "Can't delete this Catagory"}, status=201)

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
        catagory_id = data.get('category')

        category = get_object_or_404(Category, pk=catagory_id)

        products = Product.objects.create(name=name, rate=rate, category=category)
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
        query = Product.objects.all()
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
            catagory_name = get_object_or_404(Category, pk=i.category.id)
            data.append({'id': i.id, 'name': i.name, 'rate': i.rate, 'category':catagory_name.name})

        return JsonResponse([{"total_page": number_of_pages}] + data, safe=False)

# =======================
# ===== Update Products
# =======================
@api_view(['PUT'])
def update_products(request, pk):
    products = get_object_or_404(Product, pk=pk)
    serializer = ProductsSerializer(products, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# =======================
# ===== Delete Products
# =======================
def delete_products(request, pk):
    products = get_object_or_404(Product, pk=pk)
    try:
        products.delete()
    except IntegrityError:
        return JsonResponse({'message': "Can't delete this Product"}, status=201)
    
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

        products_id = data.get('product')
        employee_id = data.get('employee')
        quantity = data.get('quantity')
        rate = data.get('rate')
        current_status = "IN-STOCK"

        product = get_object_or_404(Product, pk=products_id)
        employee = get_object_or_404(Employee, pk=employee_id)

        production = Production.objects.create(product=product, employee=employee, quantity=quantity, rate=rate)
        production.save()

        # add data in inventory
        inventory = Inventory.objects.create(employee=employee, product=product, production=production, current_status=current_status)
        inventory.save()
        
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
            data.append({'id': i.id, 'product':{'id': i.product.id, 'name':i.product.name, 'rate':i.rate}, "employee":{'id':i.employee.id, 'name':i.employee.name}, "quantity":i.quantity, 'rate': i.rate, 'payment':i.payment,'date': i.created_at.date()})

        return JsonResponse([{"total_page": number_of_pages}] + data, safe=False)

# ========================
# ===== Update Production
# ========================
@api_view(['PUT'])
def update_production(request, pk):
    production = get_object_or_404(Production, pk=pk)
    serializer = ProductionSerializer(production, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# =======================
# ===== Delete Production
# =======================
def delete_production(request, pk):
    production = get_object_or_404(Production, pk=pk)
    try:
        production.delete()
    except IntegrityError:
        return JsonResponse({'message': "Can't remove it from production"}, status=201)
    return JsonResponse({'message': 'Removed Productions from database.'}, status=201)




# ====================== Inventory Section =====================
# =======================
# ===== Add to Inventory
# =======================
@csrf_exempt
def add_inventory(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        production = data.get('production')
        current_status = data.get('current_status')

        production = get_object_or_404(Production, pk=production)
        employee = get_object_or_404(Employee, pk=production.employee_id)
        product = get_object_or_404(Product, pk=production.product.id)


        inventory = Inventory.objects.create(employee=employee, product=product, production=production, current_status=current_status)
        inventory.save()
        
        return JsonResponse({'message': 'Production added to Inventory'}, status=201)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)



# =======================
# ===== View Inventory
# =======================
def view_inventory(request, pk):
    data = []
    limit = 10
    offset = (pk - 1) * limit

    # Count total records for pagination
    total_records = Inventory.objects.count()
    number_of_pages = ceil(total_records / limit)

    # Get the filtered records for the current page
    inventory_items = Inventory.objects.select_related('product', 'employee', 'production').all()[offset:offset + limit]

    # Variables
    sl_no = offset + 1  # Start numbering based on the offset
    for item in inventory_items:
        data.append({
            'id': item.id,
            'product': {
                'id': item.product.id, 
                'name': item.product.name
            },
            'employee': {
                'id': item.employee.id, 
                'name': item.employee.name
            },
            'production': item.production.id,
            'quantity': item.production.quantity,
            'status': item.current_status,
            'date': item.created_at
        })
        sl_no += 1

    # Return JSON response with pagination and data
    return JsonResponse([{"total_page": number_of_pages}] + data, safe=False)

# ========================
# ===== Update Inventory
# ========================
@api_view(['PUT'])
def update_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    serializer = InventorySerializer(inventory, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# =======================
# ===== Delete Inventory
# =======================
def delete_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    try:
        inventory.delete()
    except IntegrityError:
        return JsonResponse({'message': "Can't remove it from inventory"}, status=201)

    return JsonResponse({'message': 'Removed Inventory from database.'}, status=201)




# ===================================== Filter Inventory Section =====================================
@csrf_exempt
def filter_inventory(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)


        product = data.get('product')
        employee = data.get('employee')


        if product != '' and employee == '':
            try:
                product_instinct = get_object_or_404(Product, pk=product)
            except Http404:
                return JsonResponse({"error": "No product matches the given query"}, status=404)
            
            inventory_records = Inventory.objects.filter(
                product = product_instinct,
                current_status = 'IN-STOCK'
            )
        
        elif employee != '' and product == '':
            try:
                employee_instinct = get_object_or_404(Employee, pk=employee)
            except Http404:
                 return JsonResponse({"error": "No product matches the given query"}, status=404)
            
            inventory_records = Inventory.objects.filter(
                employee = employee_instinct,
                current_status = 'IN-STOCK'
            )

        elif employee != '' and product != '':
            try:
                employee_instinct = get_object_or_404(Employee, pk=employee)
                product_instinct = get_object_or_404(Product, pk=product)
            except Http404:
                 return JsonResponse({"error": "No product matches the given query"}, status=404)
            
            inventory_records = Inventory.objects.filter(
                employee = employee_instinct,
                product = product_instinct,
                current_status = 'IN-STOCK'
            )

        else:
            inventory_records = Inventory.objects.filter(
                current_status = 'IN-STOCK'
            )


        data = []

        for i in inventory_records:
            data.append({
                'id': i.id,
                'employee':{
                    'id':i.employee.id,
                    'name':i.employee.name
                },
                'product':{
                    'id':i.product.id,
                    'name': i.product.name
                },
                'production':{
                    'id':i.production.id,
                    'quantity':i.production.quantity
                }
            })

        return JsonResponse(data, safe=False, status=201)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)



