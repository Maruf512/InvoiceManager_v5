from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from ..models import Product, Employee, Inventory
import json



def FilterInventory(request):
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
                current_status = 'IN-STOCK')
        
        elif employee != '' and product == '':
            try:
                employee_instinct = get_object_or_404(Employee, pk=employee)
            except Http404:
                 return JsonResponse({"error": "No product matches the given query"}, status=404)
            
            inventory_records = Inventory.objects.filter(
                employee = employee_instinct,
                current_status = 'IN-STOCK')

        elif employee != '' and product != '':
            try:
                employee_instinct = get_object_or_404(Employee, pk=employee)
                product_instinct = get_object_or_404(Product, pk=product)
            except Http404:
                 return JsonResponse({"error": "No product matches the given query"}, status=404)
            
            inventory_records = Inventory.objects.filter(
                employee = employee_instinct,
                product = product_instinct,
                current_status = 'IN-STOCK')

        else:
            inventory_records = Inventory.objects.filter(
                current_status = 'IN-STOCK')

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
    