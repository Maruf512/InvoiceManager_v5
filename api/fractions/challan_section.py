from ..models import Inventory, Customer, Challan, ChallanProduction, Production, EmployeeBillProduction, EmployeeBill
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.http import JsonResponse
from collections import defaultdict
from datetime import datetime
from math import ceil
import json


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
        date = data.get('date')
        total = 0
        current_status = "NOT-PAID"

        for item in inventory_id:
            inventory = get_object_or_404(Inventory, pk=item)
            total += inventory.production.quantity

        challan = Challan.objects.create(customer=customer, total=total, current_status=current_status)
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            challan.created_at = date_obj
        except ValueError:
            pass

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

    # Order by created_at in descending order to fetch the latest first
    total_records = Challan.objects.count()
    number_of_pages = ceil(total_records / limit)
    challan_items = Challan.objects.all().order_by('-id')[offset:offset + limit]

    sl_no = offset + 1 
    for item in challan_items:
        products = []
        quantity = ""
        challan_production = ChallanProduction.objects.filter(challan=item.id)
        
        for i in challan_production:
            unites = i.production.product.category.unit
            if i.production.quantity % 1 == 0:
                quantity += f"{int(i.production.quantity)} + "
            else:
                quantity += f"{i.production.quantity} + "

            if i.production.product.name not in products:
                products.append(i.production.product.name)

        # Process data
        products_name = ", ".join(products)  # Use join to concatenate product names
        quantity = quantity[:-3]  # Remove trailing ' + '

        # Add item data to the response
        data.append({
            'id': item.id,
            'customer': {'id': item.customer.id, 'name': item.customer.name},
            'products': products_name,
            'quantity': quantity,
            'total': f"{item.total} {unites}",
            'current_status': item.current_status,
            'date': item.created_at.strftime("%d %b %y")  # Format date as "13 Nov 2024"
        })
        sl_no += 1

    return JsonResponse([{"total_page": number_of_pages}] + data, safe=False)


# =======================
# ===== View Single Challan
# =======================
def ViewChallan(request, pk):
    # Fetch the Challan object or return 404 if not found
    challan = get_object_or_404(Challan, pk=pk)
    
    # Retrieve ChallanProduction entries associated with the Challan
    challan_production = ChallanProduction.objects.filter(challan=challan)

    # Use defaultdict to group data by employee and product
    production_data = defaultdict(lambda: defaultdict(list))
    
    # Group ChallanProduction data by employee and product
    for item in challan_production:
        production_data[item.production.employee.id][item.product.id].append(item)

    # Prepare the columns data for the invoice
    total_column = []
    grand_total = 0

    # Iterate over grouped data
    for employee_id, products in production_data.items():
        for product_id, items in products.items():
            # set unites
            unites = items[0].production.product.category.unit
            # Calculate total and quantities
            production_qty = ''
            total = 0
            for item in items:
                qty = int(item.production.quantity) if item.production.quantity % 1 == 0 else item.production.quantity
                production_qty += f"{qty}+"
                total += qty
                grand_total += qty

            # Add item to the total column
            total_column.append({
                'employee': items[0].production.employee.name,
                'product': items[0].product.name,
                'quantity': production_qty[:-1],  # Remove the last "+" from the quantity
                'total': f"{total} {unites}"
            })

    # Update Challan's grand total if necessary
    if challan.total != grand_total:
        challan.total = grand_total
        challan.save()

    # Gather the invoice data
    invoice_data = {
        'customer_name': challan.customer.name,
        'customer_company': challan.customer.company_name,
        'customer_address': challan.customer.address,
        'challan_no': challan.id,
        'date': challan.created_at.strftime("%d %b %y"),
        'grand_total': f"{challan.total} {unites}",
        'total_column': total_column
    }

    # Return the invoice data as a JSON response
    return JsonResponse(invoice_data, safe=False, status=201)

def DeleteChallan(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

    try:
        id = data['id']
        deleteRelatedData = data['deleteRelatedData']

        challan = get_object_or_404(Challan, pk=id)

        if deleteRelatedData == False:
            # Change inventory status
            challan_production = list(ChallanProduction.objects.filter(challan=challan).values('production'))
            for production in challan_production:
                inventory_instincts = Inventory.objects.filter(production=production.get('production')).values('id')
                inventory = get_object_or_404(Inventory, pk=inventory_instincts[0].get('id'))
                inventory.current_status = "IN-STOCK"
                inventory.save()

            # delete challan and challan production
            ChallanProduction.objects.filter(challan=challan).delete()
            challan.delete()

        elif deleteRelatedData == True:
            challan_production = list(ChallanProduction.objects.filter(challan=challan).values('production'))

            production_exists_in_payment = False

            for production in challan_production:
                production_instinct = get_object_or_404(Production, pk=production['production'])
                production_exists = EmployeeBillProduction.objects.filter(production=production_instinct).count()
                if production_exists > 0:
                    production_exists_in_payment = True




            if production_exists_in_payment == False:
                for production in challan_production:
                    production_instinct = get_object_or_404(Production, pk=production['production'])
                    production_instinct.delete()

                ChallanProduction.objects.filter(challan=challan).delete()
                challan.delete()

            else:
                # Change inventory status
                challan_production = list(ChallanProduction.objects.filter(challan=challan.id).values('production'))
                for production in challan_production:
                    inventory_instincts = Inventory.objects.filter(production=production.get('production')).values('id')
                    inventory = get_object_or_404(Inventory, pk=inventory_instincts[0].get('id'))
                    inventory.current_status = "IN-STOCK"
                    inventory.save()

                ChallanProduction.objects.filter(challan=challan).delete()
                challan.delete()


    except IntegrityError:
        return JsonResponse({'message': "Can't remove it from Invoice"}, status=201)
    return JsonResponse({'message': 'Removed Invoice from database.'}, status=201)

