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
                    quantity=float(item.get('quantity', 0)[:-3]),
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
        single_view_data = ViewEmployeeBill(request, item.id)
        single_view_data = json.loads(single_view_data.content)

        products = ""
        quantity = ""
        total_qty = 0
        raw_data = single_view_data['data']
        unit = raw_data[0]['total_qty'].split(' ')[-1]
        for product in raw_data:
            products += product['products']
            quantity += product['quantity']
            total_qty += float(product['total_qty'][:-4])

        data.append({
            'id': item.id,
            'employee': single_view_data['employee'],
            'products': products,
            'production': quantity,
            'quantity': f"{total_qty} {unit}",
            'Amount': single_view_data['grand_total'],
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
            amount_calc = item.quantity * item.product.production_cost
            amount += amount_calc

        unites = products[0].category.unit

        bill_data.append({'sl_no': sl_no, 'products': f"{products[0].name}", 'quantity':f"{product_qty[:-2]}", 'total_qty':f"{total_qty} {unites}", 'rate':int(item.product.production_cost) if item.product.production_cost % 1 == 0 else item.product.production_cost,'amount': int(amount) if amount % 1 == 0 else amount})
        sl_no += 1


    # to show grand total
    grand_total = 0
    for i in bill_data:
        grand_total += i['amount']

    return JsonResponse({'date': employee_bill.created_at.strftime("%d %b %y"), 'grand_total': int(grand_total) if grand_total % 1 == 0 else grand_total, 'employee':{'id': employee_bill.employee.id, 'name': employee_bill.employee.name}, 'data':bill_data}, safe=False, status=201)
