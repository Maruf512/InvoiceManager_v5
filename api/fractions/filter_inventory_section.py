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

        # Retrieve filters
        product_id = data.get('product')
        employee_id = data.get('employee')

        # Base queryset
        inventory_records = Inventory.objects.filter(current_status='IN-STOCK')

        # Apply product filter if provided
        if product_id:
            try:
                product_instance = get_object_or_404(Product, pk=product_id)
                inventory_records = inventory_records.filter(product=product_instance)
            except Http404:
                return JsonResponse({"error": "No product matches the given query."}, status=404)

        # Apply employee filter if provided
        if employee_id:
            try:
                employee_instance = get_object_or_404(Employee, pk=employee_id)
                inventory_records = inventory_records.filter(employee=employee_instance)
            except Http404:
                return JsonResponse({"error": "No employee matches the given query."}, status=404)

        # Prepare response data
        data = []
        for record in inventory_records:
            data.append({
                'id': record.id,
                'employee': {
                    'id': record.employee.id,
                    'name': record.employee.name
                },
                'product': {
                    'id': record.product.id,
                    'name': record.product.name
                },
                'production': {
                    'id': record.production.id,
                    'quantity': f"{int(record.production.quantity) if record.production.quantity % 1 == 0 else record.production.quantity} {record.production.product.category.unit}"
                }
            })

        return JsonResponse(data, safe=False, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
