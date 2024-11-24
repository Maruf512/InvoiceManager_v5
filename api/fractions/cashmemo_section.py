from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ..models import Challan, ChallanProduction, Customer, CashMemo, CashMemoChallan, Product
from math import ceil
import json


def CashMemoFilter(request, pk):
    if not pk:
        return JsonResponse({'error': 'Customer ID is required.'}, status=400)

    customer_instinct = get_object_or_404(Customer, pk=pk)

    data = []

    challan_items = Challan.objects.all().filter(
        current_status="NOT-PAID",
        customer = customer_instinct
    ).order_by('-created_at')

    for item in challan_items:
        products = []
        quantity = ""
        amount = 0
        challan_production = ChallanProduction.objects.filter(challan=item.id)
        
        for i in challan_production:
            if i.production.quantity % 1 == 0:
                quantity += f"{int(i.production.quantity)} + "
            else:
                quantity += f"{i.production.quantity} + "


            amount += i.product.rate * i.production.quantity


            if i.production.product.name not in products:
                products.append(i.production.product.name)

        # Process data
        products_name = ", ".join(products)  # Use join to concatenate product names
        quantity = quantity[:-3]  # Remove trailing ' + '

        # Add item data to the response
        data.append({
            'id': item.id,
            'products': products_name,
            'quantity': quantity,
            'total': f"{item.total} yds",
            'amount': f"{int(amount) if amount % 1 == 0 else amount}/=",
            'current_status': item.current_status,
            'date': item.created_at.strftime("%d %b %y")  # Format date as "13 Nov 2024"
        })

    return JsonResponse(data, safe=False, status=200)


def AddCashMemo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        print(data.get('challan'))

        total_qty = 0
        amount = 0
        challan_production_data = []
        for challan_id in data['challan']:
            challan_instinct = get_object_or_404(Challan, pk=challan_id)
            challan_production_instinct = ChallanProduction.objects.filter(challan_id=challan_instinct)

            
            for challan in challan_production_instinct:
                rate = challan.product.rate
                quantity = challan.production.quantity
                amount += rate * quantity
                print(challan.production.product.name)
                challan_production_data.append({'product_id': challan.product, 'challan_id': challan.challan})

            customer = challan_instinct.customer.id
            total_qty += float(challan_instinct.total)
            
        print(f"customer: {customer}, total_yds: {total_qty}, total_amount: {amount}")

        cashmemo = CashMemo.objects.create(
            customer = get_object_or_404(Customer, pk= customer),
            total_yds = total_qty,
            total_amount = amount
        )


        for item in challan_production_data:
            cashmemo_challan = CashMemoChallan.objects.create(
                cashmemo = cashmemo,
                product = get_object_or_404(Product, pk=item['product_id'].id),
                challan = get_object_or_404(Challan, pk=item['challan_id'].id)
            )

        return JsonResponse({'message':'added successfully'}, status=200)


    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)