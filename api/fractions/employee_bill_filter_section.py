from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from ..models import Production, Employee, ChallanProduction, Challan
import json


def EmployeeBillFilter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        employee_id = data.get('employee')
        filter_method = data.get('filter_method', '').lower()

        # Validate employee
        try:
            employee_instance = get_object_or_404(Employee, pk=employee_id)
        except Http404:
            return JsonResponse({"error": "No Employee matches the given query"}, status=404)

        filtered_data = []

        # **Production-based Filter**
        if filter_method == "production":
            production_records = Production.objects.filter(
                payment="NOT-PAID",
                employee=employee_instance
            )

            for item in production_records:
                # Handle Decimal Points
                rate = int(item.rate) if item.rate % 1 == 0 else item.rate
                quantity = int(item.quantity) if item.quantity % 1 == 0 else item.quantity

                filtered_data.append({
                    'id': item.id,
                    'employee': {
                        'id': item.employee.id,
                        'name': item.employee.name
                    },
                    'product': {
                        'id': item.product.id,
                        'name': item.product.name,
                        'category': item.product.category.name
                    },
                    'quantity': quantity,
                    'rate': rate,
                    'amount': quantity * rate
                })

        # **Challan-based Filter**
        elif filter_method == "challan":
            challan_ids = data.get('challan', [])

            if not isinstance(challan_ids, list):
                return JsonResponse({'error': 'Challan must be a list.'}, status=400)

            for challan_id in challan_ids:
                try:
                    challan_instance = get_object_or_404(Challan, pk=challan_id)
                except Http404:
                    return JsonResponse({'error': f'Challan with id {challan_id} not found.'}, status=404)

                challan_production_records = ChallanProduction.objects.filter(
                    challan=challan_instance,
                    employee=employee_instance,
                    production__payment="NOT-PAID"
                )

                for item in challan_production_records:
                    quantity = int(item.production.quantity) if item.production.quantity % 1 == 0 else item.production.quantity
                    rate = int(item.production.rate) if item.production.rate % 1 == 0 else item.production.rate

                    filtered_data.append({
                        'id': item.production.id,
                        'employee': {
                            'id': item.employee.id,
                            'name': item.employee.name
                        },
                        'product': {
                            'id': item.production.product.id,
                            'name': item.production.product.name,
                            'category': item.production.product.category.name
                        },
                        'challan': {
                            'id': item.challan.id,
                            'date': item.challan.created_at.strftime("%d %b %y")  # Fixed formatting
                        },
                        'quantity': quantity,
                        'rate': rate,
                        'amount': quantity * rate
                    })

        else:
            return JsonResponse({'error': 'Invalid filter method.'}, status=400)

        return JsonResponse(filtered_data, safe=False, status=200)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
