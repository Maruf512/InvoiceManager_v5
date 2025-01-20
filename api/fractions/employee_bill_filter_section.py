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

        # Retrieve the employee and filter method from the data
        employee_id = data.get('employee')
        filter_method = data.get('filter_method', '').lower()

        # Validate presence of employee ID and filter method
        if not employee_id:
            return JsonResponse({'error': 'Employee ID is required.'}, status=400)

        if filter_method not in ["production", "challan"]:
            return JsonResponse({'error': 'Invalid filter method. Must be "production" or "challan".'}, status=400)

        # Fetch employee instance or return 404 if not found
        try:
            employee_instance = get_object_or_404(Employee, pk=employee_id)
        except Http404:
            return JsonResponse({"error": "Employee not found."}, status=404)

        filtered_data = []

        # **Production-based Filter**
        if filter_method == "production":
            production_records = Production.objects.filter(
                payment="NOT-PAID",
                employee=employee_instance
            )

            if not production_records:
                return JsonResponse({'message': 'No production records found for this employee.'}, status=200)

            for item in production_records:
                # Handle Decimal Points
                rate = int(item.product.rate) if item.product.rate % 1 == 0 else item.product.rate
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
                    'quantity': f"{quantity} { item.product.category.unit}",
                    'rate': rate,
                    'amount': quantity * rate,
                    'date': item.created_at.strftime("%d %b %y")
                })

        # **Challan-based Filter**
        elif filter_method == "challan":
            challan_ids = data.get('challan', [])

            if not isinstance(challan_ids, list):
                return JsonResponse({'error': 'Challan must be provided as a list.'}, status=400)

            if not challan_ids:
                return JsonResponse({'error': 'Challan list cannot be empty.'}, status=400)

            for challan_id in challan_ids:
                try:
                    challan_instance = get_object_or_404(Challan, pk=challan_id)
                except Http404:
                    # Instead of returning an error, just skip this challan_id if not found
                    continue

                # Now check if the employee has relevant data in the challan
                challan_production_records = ChallanProduction.objects.filter(
                    challan=challan_instance,
                    employee=employee_instance,
                    production__payment="NOT-PAID"
                )

                # If no relevant data for the employee in this challan, skip it
                if not challan_production_records:
                    continue  # Skip this challan and move to the next one

                # Process records if found
                for item in challan_production_records:
                    quantity = int(item.production.quantity) if item.production.quantity % 1 == 0 else item.production.quantity
                    rate = int(item.production.product.rate) if item.production.product.rate % 1 == 0 else item.production.product.rate

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
                        'quantity': f"{quantity} { item.production.product.category.unit}",
                        'rate': rate,
                        'amount': quantity * rate,
                        'date': item.challan.created_at.strftime("%d %b %y")
                    })

        # Return filtered data or a message if no data found
        if not filtered_data:
            return JsonResponse({'message': 'No records found matching the filter criteria.'}, status=200)

        return JsonResponse(filtered_data, safe=False, status=200)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

