from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from ..models import Product, Employee, Production, Inventory
from ..serializer import ProductionSerializer
import json


# =======================
# ===== Add Production
# =======================
def AddProduction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        products_id = data.get('product')
        employee_id = data.get('employee')
        quantity = data.get('quantity')
        current_status = "IN-STOCK"

        product = get_object_or_404(Product, pk=products_id)
        employee = get_object_or_404(Employee, pk=employee_id)

        production = Production.objects.create(product=product, employee=employee, quantity=quantity, rate=product.production_cost)
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
def ViewProduction(request, pk):
    data = []
    if pk > 0:
        query = Production.objects.all().order_by('-id')
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
            data.append({'id': i.id, 'product':{'id': i.product.id, 'name':i.product.name, 'rate':i.product.rate}, "employee":{'id':i.employee.id, 'name':i.employee.name}, "quantity":f"{int(i.quantity) if i.quantity % 1 == 0 else i.quantity} {i.product.category.unit}", 'rate': i.product.rate, 'payment':i.payment,'date': i.created_at.date().strftime("%d %b %y")})


        return JsonResponse([{"total_page": number_of_pages}] + data, safe=False)


# ========================
# ===== Update Production
# ========================
def UpdateProduction(request, pk):
    production = get_object_or_404(Production, pk=pk)
    serializer = ProductionSerializer(production, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =======================
# ===== Delete Production
# =======================
def DeleteProduction(request, pk):
    production = get_object_or_404(Production, pk=pk)
    try:
        production.delete()
    except IntegrityError:
        return JsonResponse({'message': "Can't remove it from production"}, status=201)
    return JsonResponse({'message': 'Removed Productions from database.'}, status=201)
