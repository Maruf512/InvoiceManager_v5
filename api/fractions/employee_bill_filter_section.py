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
        
        employee = data.get('employee')
        filter_method = data.get('filter_method').lower()

        try:
            employee_instincts = get_object_or_404(Employee, pk=employee)
        except Http404:
            return JsonResponse({"error": "No Employee matches the given query"}, status=404)

        filtered_data = []
        # For Production based Filter
        if filter_method == "production":
            production_records = Production.objects.filter(
                payment = "NOT-PAID",
                employee = employee_instincts)

            for item in production_records:
                # Handel Decimal points
                if item.rate % 1 == 0:
                    rate = int(item.rate)
                else:
                    rate = item.rate
                
                if item.quantity % 1 == 0:
                    quantity = int(item.quantity)
                else:
                    quantity = item.quantity

                filtered_data.clear()
                filtered_data.append({
                    'id': item.id,
                    'employee':{
                        'id': item.employee.id,
                        'name': item.employee.name },
                    'product':{
                        'id': item.product.id,
                        'name': item.product.name,
                        'catagory': item.product.category.name},
                    'quantity': quantity,
                    'rate': rate,
                    'amount': quantity * rate
                })

        # For challan based Filter
        else:
            filtered_data.clear()
            challan_id = data.get('challan')

            for challan in challan_id:
                challan_instincts = get_object_or_404(Challan, pk=challan)

                challan_production_records = ChallanProduction.objects.filter(
                    challan_id = challan_instincts,
                    employee_id = employee_instincts,
                    production_id__payment = "NOT-PAID"
                    )

                for item in challan_production_records:
                    if item.production.quantity % 1 == 0:
                        quantity = int(item.production.quantity)
                    else:
                        quantity = item.production.quantity
                    
                    if item.production.rate % 1 == 0:
                        rate = int(item.production.rate)
                    else:
                        rate = item.production.rate
                    
                    filtered_data.append({
                        'id': item.production.id,
                        'employee':{
                            'id': item.employee.id,
                            'name': item.employee.name },
                        'product':{
                            'id': item.product.id,
                            'name': item.product.name,
                            'catagory': item.product.category.name},
                        'challan':{
                            'id': item.challan.id,
                            'date': f"{item.created_at.date()}"
                        },
                        'quantity': quantity,
                        'rate': rate,
                        'amount': quantity * rate
                    })

        return JsonResponse(filtered_data, safe=False, status=200)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
