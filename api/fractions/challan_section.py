from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ..models import Inventory, Customer, Challan, ChallanProduction
import json
from math import ceil


# =======================
# ===== Create Challan
# =======================
def AddChallan(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        
        inventory_id = data.get('inventory_id')
        customer = get_object_or_404(Customer, pk=data.get("customer_id"))
        total = 0
        current_status = "NOT-PAID"

        for item in inventory_id:
            inventory = get_object_or_404(Inventory, pk=item)
            total += inventory.production.quantity

        challan = Challan.objects.create(customer=customer, total=total, current_status=current_status)
        challan.save()

        for item in inventory_id:
            inventory = get_object_or_404(Inventory, pk=item)
            inventory.current_status = "OUT-OF-STOCK"
            inventory.save()
            challan_production = ChallanProduction.objects.create(challan=challan, employee=inventory.employee, product=inventory.product, production=inventory.production )
            challan_production.save()

        return JsonResponse({"message": "Data saved successfully", "challan_id": challan.id}, safe=False, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    

# =======================
# ===== View All Challan
# =======================
def ViewAllChallan(request, pk):
    data = []
    limit = 10
    offset = (pk - 1) * limit

    total_records = Challan.objects.count()
    number_of_pages = ceil(total_records / limit)
    challan_items = Challan.objects.all()[offset:offset + limit]

    sl_no = offset + 1 
    for item in challan_items:
        products = []
        quantity = ""
        challan_production = ChallanProduction.objects.filter(challan = item.id)
        
        for i in challan_production:
            if i.production.quantity % 1 == 0:
                quantity += f"{int(i.production.quantity)} + "
            else:
                quantity += f"{i.production.quantity} + "
            

            if i.production.product.name not in products:
                products.append(i.production.product.name)

        # process data
        products_name = ""
        for product in products:
            products_name += f"{product}, "

        products_name = products_name[:-2]
        quantity = quantity[:-3]
        

        data.append({'id':item.id, 'products': products_name, "quantity":quantity,'total': f"{item.total} yds", 'current_status': item.current_status, 'date': item.created_at.date()})
        sl_no += 1

    return JsonResponse([{"total_page": number_of_pages}] + data, safe=False)


# =======================
# ===== View Single Challan
# =======================
def ViewChallan(request, pk):
    challan = get_object_or_404(Challan, pk=pk)
    # Veriables
    challan_production_products = []
    challan_production_employee = []
    data = []
    
    challan_production = ChallanProduction.objects.filter(challan = challan.id)
    for item in challan_production:
        if item.product.id not in challan_production_products:
            challan_production_products.append(item.product.id)
        
        if item.production.employee.id not in challan_production_employee:
            challan_production_employee.append(item.production.employee.id)

    for employee in challan_production_employee:
        for product in challan_production_products:
            challan_production_filter = ChallanProduction.objects.filter(
                challan = challan.id,
                employee = employee,
                product = product
            )

            data.append({'colum': challan_production_filter})

    # gather all the data
    total_column = []
    customer_name = challan.customer.name
    customer_address = challan.customer.address
    customer_company = challan.customer.company_name
    date = challan.created_at.date()
    challan_no = challan.id
    grand_total = 0
    
    for item in data:
        production_qty = ""
        total = 0
        for i in item['colum']:
            if i.production.quantity % 1 == 0:
                production_qty += f"{int(i.production.quantity)}+"
            else:
                production_qty += f"{i.production.quantity}+"

            total += i.production.quantity
            grand_total += i.production.quantity

        total_column.append({'employee': item['colum'][0].employee.name, 'product':item['colum'][0].product.name, 'quantity':production_qty[:-1], 'total': total})

    # update challan grand total
    if challan.total != grand_total:
        challan.total = grand_total
        challan.save()

    invoice_data = {
        'customer_name': customer_name,
        'customer_company': customer_company,
        'customer_address': customer_address,
        'challan_no': challan_no,
        'date': f"{date}",
        'grand_total': challan.total,
        'total_column': total_column
    }

    return JsonResponse(invoice_data, safe=False, status=201)
