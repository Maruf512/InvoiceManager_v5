from ..models import Customer, Employee, Product, Production, Challan, ChallanProduction, Inventory
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db import transaction
import json


def SimpleInvoice(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        try:
            with transaction.atomic():  # Start a transaction block
                # Get customer data
                customer_instinct = get_object_or_404(Customer, pk=data.get('customer'))

                # Extract data from production list
                production_list = data.get('production')

                # Saved production and inventory IDs
                saved_production = []
                saved_inventory = []
                total_qty = 0

                for production in production_list:
                    # Process employee and product instances
                    employee_instinct = get_object_or_404(Employee, pk=production.get('employee'))
                    product_instinct = get_object_or_404(Product, pk=production.get('product'))

                    # Parse quantities
                    qty_list = production.get('qty').strip().split('+')
                    for qty in qty_list:
                        # Create production instance
                        production_instinct = Production.objects.create(
                            product=product_instinct,
                            employee=employee_instinct,
                            quantity=qty,
                            rate=product_instinct.production_cost
                        )
                        saved_production.append(production_instinct)

                        # Add production to inventory
                        inventory_instinct = Inventory.objects.create(
                            employee=employee_instinct,
                            product=product_instinct,
                            production=production_instinct,
                            current_status="IN-STOCK"
                        )
                        saved_inventory.append(inventory_instinct)

                        # Update total quantity
                        total_qty += float(qty)

                # Create challan
                challan_instinct = Challan.objects.create(
                    customer=customer_instinct,
                    total=total_qty,
                    current_status="NOT-PAID"
                )

                # Create challanProduction entries and update inventory
                for item in saved_inventory:
                    item.current_status = "OUT-OF-STOCK"
                    item.save()
                    ChallanProduction.objects.create(
                        challan=challan_instinct,
                        employee=item.employee,
                        product=item.product,
                        production=item.production
                    )

            # Return challan ID
            return JsonResponse({"message": "Data saved successfully", "challan_id": challan_instinct.id}, safe=False,
                                status=200)

        except Exception as e:
            # Catch and return any error
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
