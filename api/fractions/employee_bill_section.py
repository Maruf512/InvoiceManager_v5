from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from ..models import Production, EmployeeBill, EmployeeBillProduction, Product
from django.db import transaction
from math import ceil
import json


def AddEmployeeBill(request):
    if request.method != 'POST':
        return JsonResponse({'error': "Invalid Request Method."}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

    # Begin transaction to ensure atomicity
    try:
        with transaction.atomic():
            employee_id = data[0].get('employee', {}).get('id')
            if not employee_id:
                return JsonResponse({'error': 'Employee ID is missing.'}, status=400)

            total_amount = sum(item.get('amount', 0) for item in data)
            employee_bill_record = EmployeeBill.objects.create(
                employee_id=employee_id,
                total_amount=total_amount,
                current_status="PAID"
            )

            for item in data:
                product_id = item.get('product', {}).get('id')
                production_id = item.get('id')
                
                if not product_id or not production_id:
                    return JsonResponse({'error': 'Invalid product or production data.'}, status=400)

                product_instinct = get_object_or_404(Product, pk=product_id)
                production_instinct = get_object_or_404(Production, pk=production_id)

                # Update production payment status
                production_instinct.payment = "PAID"
                production_instinct.save()

                # Create EmployeeBillProduction record
                EmployeeBillProduction.objects.create(
                    employee_bill_id=employee_bill_record,
                    product=product_instinct,
                    production=production_instinct,
                    rate=item.get('rate', 0),
                    quantity=item.get('quantity', 0),
                    amount=item.get('amount', 0)
                )

        return JsonResponse({'message': "Employee Bill Saved.", 'bill_id': employee_bill_record.id}, status=200)

    except Exception as e:
        return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)


def ViewAllEmployeeBill(request, pk):
    data = []
    limit = 10
    offset = (pk - 1) * limit

    # Order by created_at in descending order to fetch the latest first
    total_records = EmployeeBill.objects.count()
    number_of_pages = ceil(total_records / limit)
    employee_bill_items = EmployeeBill.objects.all().order_by('-created_at')[offset:offset + limit]

    for item in employee_bill_items:
        products = []
        production = ""
        quantity = 0
        employee_bill_production = EmployeeBillProduction.objects.filter(employee_bill_id=item.id)
        
        for i in employee_bill_production:
            if i.production.quantity % 1 == 0:
                production += f"{int(i.production.quantity)} + "
                quantity += int(i.production.quantity)
            else:
                production += f"{i.production.quantity} + "
                quantity += i.production.quantity

            if i.production.product.name not in products:
                products.append(i.production.product.name)

        # Process data
        products_name = ", ".join(products)  # Use join to concatenate product names
        production = production[:-3]  # Remove trailing ' + '

        # Add item data to the response
        data.append({
            'id': item.id,
            'employee': {'id':item.employee.id, 'name': item.employee.name},
            'products': products_name,
            'production': production,
            'quantity': f"{quantity} yds",
            'Amount': f"{item.total_amount}/=",
            'current_status': item.current_status,
            'date': item.created_at.strftime("%d %b %y")
        })


    return JsonResponse([{"total_page": number_of_pages}] + data, safe=False)

