from ..models import Challan, ChallanProduction, Customer, CashMemo, CashMemoChallan, Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from collections import defaultdict
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
    ).order_by('-id')

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
                challan_production_data.append({'product_id': challan.product, 'challan_id': challan.challan})

            customer = challan_instinct.customer.id
            total_qty += float(challan_instinct.total)

        cashmemo = CashMemo.objects.create(
            customer = get_object_or_404(Customer, pk=customer),
            total_yds = total_qty,
            total_amount = amount
        )


        for item in challan_production_data:
            cashmemo_challan = CashMemoChallan.objects.create(
                cashmemo = cashmemo,
                product = get_object_or_404(Product, pk=item['product_id'].id),
                challan = get_object_or_404(Challan, pk=item['challan_id'].id)
            )
            invoice = Challan.objects.get(id=item['challan_id'].id)
            invoice.current_status = "PAID"
            invoice.save()

        return JsonResponse({'message':'added successfully'}, status=200)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    

def ViewAllCashmemo(request, pk):
    data = []
    limit = 10
    offset = (pk - 1) * limit

    # Order by created_at in descending order to fetch the latest first
    total_records = CashMemo.objects.count()
    number_of_pages = ceil(total_records / limit)
    cashmemo_items = CashMemo.objects.all().order_by('-id')[offset:offset + limit]

    for item in cashmemo_items:
        products = []
        challan = []
        cashmemo_challan = CashMemoChallan.objects.filter(cashmemo=item.id).select_related('product', 'challan')

        for i in cashmemo_challan:
            if i.product.name not in products:
                products.append(i.product.name)
            
            if i.challan.id not in challan:
                challan.append(i.challan.id)

        data.append({
            'id': item.id,
            'customer': {'id': item.customer.id, 'name': item.customer.name},
            'challan_no': challan,
            'products': products,
            'total_qty': item.total_yds,
            'amount': item.total_amount,
            'date': item.created_at.strftime("%d %b %y")
        })

    return JsonResponse([{"total_page": number_of_pages}] + data, safe=False)


def SingleViewCashmemo(request, pk):
    memo = get_object_or_404(CashMemo, pk=pk)
    memo_challan = CashMemoChallan.objects.filter(cashmemo=memo).select_related('product', 'challan')

    # Use default-dict to group data by product and Challan
    challan_data = defaultdict(lambda: defaultdict(list))
    for item in memo_challan:
        challan_data[item.product.id][item.challan.id].append(item)

    return_data = []
    data = []
    for product, challan in challan_data.items():
        challan_list = []
        for item in challan:
            challan_list.append(item)

        data.append([product, challan_list])

    slno = 1
    total_amount = 0
    for i in data:
        product = i[0]
        challan = i[1]
        product_instinct = get_object_or_404(Product, pk=product)
        quantity = 0
        for item in challan:
            challan_production_instinct = ChallanProduction.objects.filter(challan=item, product=product_instinct)
            # get quantity
            for challan_production in challan_production_instinct:
                quantity += challan_production.production.quantity

        amount = int(product_instinct.rate * quantity) if (product_instinct.rate * quantity) % 1 == 0 else (product_instinct.rate * quantity)
        return_data.append({'slno': slno, 'products': product_instinct.name, 'challan': challan, 'quantity': int(quantity) if quantity % 1 == 0 else quantity, 'rate': product_instinct.rate, 'amount': amount})
        total_amount += amount
        slno += 1

    return JsonResponse([{'customer': memo.customer.name, 'address': memo.customer.address, 'date': memo.created_at.strftime("%d %b %y"), 'memo_id':memo.id, 'total_amount':total_amount}] + return_data, safe=False, status=200)



