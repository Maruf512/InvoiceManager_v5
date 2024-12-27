from ..models import Production, EmployeeBill, EmployeeBillProduction, Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from collections import defaultdict
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
                    quantity=int(item.get('quantity', 0)[:3]),
                    amount=item.get('amount', 0)
                )

        return JsonResponse({'message': "Employee Bill Saved.", 'bill_id': employee_bill_record.id}, status=200)

    except Exception as e:
        return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)


def ViewAllEmployeeBill(request, pk):
    data = []
    limit = 10
    offset = (pk - 1) * limit

    total_records = EmployeeBill.objects.count()
    number_of_pages = ceil(total_records / limit)
    employee_bill_items = EmployeeBill.objects.all().order_by('-id')[offset:offset + limit]

    for item in employee_bill_items:
        products = []
        production = ""
        quantity = 0
        employee_bill_production = EmployeeBillProduction.objects.filter(employee_bill_id=item.id)
        unites = ''
        for i in employee_bill_production:
            unites = i.production.product.category.unit
            if i.production.quantity % 1 == 0:
                production += f"{int(i.production.quantity)} + "
                quantity += int(i.production.quantity)
            else:
                production += f"{i.production.quantity} + "
                quantity += i.production.quantity

            if i.production.product.name not in products:
                products.append(i.production.product.name)

        products_name = ", ".join(products)
        production = production[:-3]

        data.append({
            'id': item.id,
            'employee': {'id':item.employee.id, 'name': item.employee.name},
            'products': products_name,
            'production': production,
            'quantity': f"{int(quantity) if quantity % 1 == 0 else quantity} {unites}",
            'Amount': int(item.total_amount) if item.total_amount % 1 == 0 else item.total_amount,
            'current_status': item.current_status,
            'date': item.created_at.strftime("%d %b %y")
        })

    return JsonResponse([{"total_page": number_of_pages}] + data, safe=False)


def ViewEmployeeBill(request, pk):
    employee_bill = get_object_or_404(EmployeeBill, pk=pk)
    employee_bill_production = EmployeeBillProduction.objects.filter(employee_bill_id=employee_bill.id)

    production_data = defaultdict(lambda: defaultdict(list))
    
    for item in employee_bill_production:
        production_data[item.product][item.production].append(item)

    bill_data = []
    sl_no = 1
    for products in production_data.items():
        product_qty = ""
        amount = 0
        total_qty = 0
        for item in products[1]:
            product_qty += f"{int(item.quantity) if item.quantity % 1 == 0 else item.quantity}, "
            total_qty += int(item.quantity) if item.quantity % 1 == 0 else item.quantity
            amount_calc = item.quantity * item.rate
            amount += amount_calc

        unites = products[0].category.unit

        bill_data.append({'sl_no': sl_no, 'products': f"{products[0].name}", 'quantity':f"{product_qty[:-2]}", 'total_qty':f"{total_qty} {unites}", 'rate':int(item.rate) if item.rate % 1 == 0 else item.rate,'amount': int(amount) if amount % 1 == 0 else amount})
        sl_no += 1
    
    return JsonResponse({'date': employee_bill.created_at.strftime("%d %b %y"), 'grand_total': int(employee_bill.total_amount) if employee_bill.total_amount % 1 == 0 else employee_bill.total_amount, 'employee':{'id': employee_bill.id, 'name': employee_bill.employee.name}, 'data':bill_data}, safe=False, status=201)
