from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from ..models import Product, Employee, Production, Inventory
from ..serializer import InventorySerializer
import json
from math import ceil


# =======================
# ===== Add to Inventory
# =======================
def AddInventory(request):
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
def ViewInventory(request, pk):
    data = []
    limit = 10
    offset = (pk - 1) * limit

    # Count total records for pagination
    total_records = Inventory.objects.count()
    number_of_pages = ceil(total_records / limit)

    # Get the filtered records for the current page
    inventory_items = Inventory.objects.all().order_by('-id')
    inventory_items = inventory_items[offset:offset + limit]

    # Variables
    sl_no = offset + 1
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
            'date': item.created_at.date().strftime("%d %b %y")
        })
        sl_no += 1

    return JsonResponse([{"total_page": number_of_pages}] + data, safe=False)

# ========================
# ===== Update Inventory
# ========================
def UpdateInventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    serializer = InventorySerializer(inventory, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# =======================
# ===== Delete Inventory
# =======================
def DeleteInventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    try:
        inventory.delete()
    except IntegrityError:
        return JsonResponse({'message': "Can't remove it from inventory"}, status=201)

    return JsonResponse({'message': 'Removed Inventory from database.'}, status=201)
