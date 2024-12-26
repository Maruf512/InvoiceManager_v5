from ..models import Challan, ChallanProduction, Customer, CashMemo, CashMemoChallan, Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from collections import defaultdict
from django.db.models import Sum
from  datetime import datetime
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
            # set units
            unit = i.production.product.category.unit
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
            'total': f"{item.total} {unit}",
            'amount': int(amount) if amount % 1 == 0 else amount,
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


        #Calculate discount
        discount = 0
        discount_method = "TK"
        if data['discount'] != 0:
            if data['discountMethod'] == 'percent':
                discount_method = "%"
                discount = data['discount']
                discount_amount = amount - (amount * discount / 100)

            elif data['discountMethod'] == 'amount':
                discount = data['discount']
                discount_amount = amount - discount

        else:
            discount_amount = amount


        cashmemo = CashMemo.objects.create(
            customer = get_object_or_404(Customer, pk=customer),
            total_yds = total_qty,
            total_amount = amount,
            discount = discount,
            discount_method = discount_method,
            total_after_discount = discount_amount,
        )

        # Process Date
        date = data.get('date')
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            cashmemo.created_at = date_obj
        except ValueError:
            pass

        challan.save()

        for item in challan_production_data:
            cashmemo_challan = CashMemoChallan.objects.create(
                cashmemo = cashmemo,
                product = get_object_or_404(Product, pk=item['product_id'].id),
                challan = get_object_or_404(Challan, pk=item['challan_id'].id)
            )
            invoice = Challan.objects.get(id=item['challan_id'].id)
            invoice.current_status = "PAID"
            invoice.save()

        return JsonResponse({'message':'added successfully', 'cashmemo': cashmemo.id}, status=200)

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
            unit = i.product.category.unit
            if i.product.name not in products:
                products.append(i.product.name)
            
            if i.challan.id not in challan:
                challan.append(i.challan.id)

        data.append({
            'id': item.id,
            'customer': {'id': item.customer.id, 'name': item.customer.name},
            'challan_no': challan,
            'products': products,
            'total_qty': f"{item.total_yds} {unit}",
            'amount': item.total_amount,
            'date': item.created_at.strftime("%d %b %y")
        })

    return JsonResponse([{"total_page": number_of_pages}] + data, safe=False)


def SingleViewCashmemo(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        memo_formate = data.get('format')

        # Formate 1
        if memo_formate == 'format1':
            memo = get_object_or_404(CashMemo, pk=pk)
            # get discount data from db
            total_after_discount = memo.total_after_discount

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
                    challan_production_instinct = ChallanProduction.objects.filter(challan=item,
                                                                                   product=product_instinct)
                    # get quantity
                    for challan_production in challan_production_instinct:
                        unit = challan_production.product.category.unit
                        quantity += challan_production.production.quantity

                amount = int(product_instinct.rate * quantity) if (product_instinct.rate * quantity) % 1 == 0 else (
                        product_instinct.rate * quantity)
                return_data.append({'slno': slno, 'products': product_instinct.name, 'challan': challan,
                                    'quantity': f"{int(quantity) if quantity % 1 == 0 else quantity} {unit}",
                                    'rate': product_instinct.rate,
                                    'amount': amount})
                total_amount += amount
                slno += 1


            return JsonResponse([{'customer': memo.customer.name, 'address': memo.customer.address,
                                  'date': memo.created_at.strftime("%d %b %y"), 'memo_id': memo.id,
                                  'total_amount': total_amount, 'total_after_discount':total_after_discount}] + return_data, safe=False, status=200)

        # Formate 2
        elif memo_formate == 'format2':

            memo = get_object_or_404(CashMemo, pk=pk)
            # get discount data from db
            total_after_discount = memo.total_after_discount

            memo_challan = CashMemoChallan.objects.filter(cashmemo=memo).select_related('product', 'challan')

            # Use default-dict to group data by product and Challan
            challan_data = defaultdict(lambda: defaultdict(list))
            for item in memo_challan:
                challan_data[item.product.id][item.challan.id].append(item)

            return_data = []
            data = []
            total_amount = 0
            for product, challan in challan_data.items():
                for item in challan:
                    print(product, item)

                    challan_instinct = get_object_or_404(Challan, pk=item)
                    product_instinct = get_object_or_404(Product, pk=product)

                    challan_production_instinct = ChallanProduction.objects.filter(challan=challan_instinct, product=product_instinct).values("production__quantity")

                    quantity = 0

                    for i in challan_production_instinct:
                        quantity += i['production__quantity']

                    total_amount += int(product_instinct.rate * quantity) if (product_instinct.rate * quantity) % 1 == 0 else (product_instinct.rate * quantity)


                    return_data.append({'challanid': challan_instinct.id,
                                        'products': f"{product_instinct.name}",
                                        'date': f"{challan_instinct.created_at.strftime("%d %b %y")}",
                                        'quantity': f"{int(quantity) if quantity % 1 == 0 else quantity} {product_instinct.category.unit}",
                                        'rate': int(product_instinct.rate) if product_instinct.rate % 1 == 0 else product_instinct.rate,
                                        'amount': total_amount})

            return JsonResponse([{'customer': memo.customer.name, 'address': memo.customer.address,
                                  'date': memo.created_at.strftime("%d %b %y"), 'memo_id': memo.id,
                                  'total_amount': total_amount,
                                  'total_after_discount': total_after_discount}] + return_data, safe=False, status=200)
        else:
            pass




        return JsonResponse({'message': 'Success'}, status=200)


    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

