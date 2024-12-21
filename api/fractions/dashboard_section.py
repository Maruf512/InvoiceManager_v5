from django.db.models import Sum
from ..models import EmployeeBill, Production, Employee, Challan, Product, Category, Inventory, Customer
from datetime import datetime
from django.http import JsonResponse

def ViewDashboard(request):
    # Current Month
    current_month = datetime.now().month

    # ============================ Overview ==========================
    # Employees Count
    total_employee = Employee.objects.count()

    # Customers Count
    total_customers = Customer.objects.count()

    # Total Inventories
    total_inventory = Inventory.objects.count()

    # Total Invoice
    total_invoice = Challan.objects.count()

    # Total Products
    total_products = Product.objects.count()

    # Total Production
    total_production = Production.objects.count()

    # Total Category
    total_category = Category.objects.count()

    # Active Employee
    activeEmployee = Production.objects.filter(created_at__month=current_month).values('employee__id').distinct().count()

    # ============================= Employee of the Month ===========================
    # Employee of the Month
    producedUnites = 0
    try:
        employee_of_the_month = EmployeeBill.objects.filter(created_at__month=current_month).values('employee__name', 'employee__id').annotate(total_payment=Sum('total_amount')).order_by('-total_payment').first()
        # producedUnites
        producedUnitesQuery = Production.objects.filter(payment="PAID", created_at__month=current_month, employee_id=employee_of_the_month['employee__id']).values("product__name").annotate(total_unites=Sum('quantity'))
        for item in producedUnitesQuery:
            producedUnites += item.get('total_unites')
    except:
        employee_of_the_month = {'employee__name': 'NONE', 'employee__id': 0, 'total_payment': 0}


    # =============================== Top 5 Employees based on Production ==========================
    try:
        top_employees = (Production.objects.values("employee__name", "employee__id").annotate(total_unites=Sum('quantity')).order_by('-total_unites'))[:5]
    except:
        total_employee = [{'employee__name': 'NONE', 'employee__id': 0, 'total_unites': 0}, {'employee__name': 'NONE', 'employee__id': 0, 'total_unites': 0}, {'employee__name': 'NONE', 'employee__id': 0, 'total_unites': 0}, {'employee__name': 'NONE', 'employee__id': 0, 'total_unites': 0}, {'employee__name': 'NONE', 'employee__id': 0, 'total_unites': 0}]


    # =============================== Invoice Section ==========================
    try:
        InvoicereceivedPayment = Challan.objects.filter(current_status='PAID').count()
    except:
        InvoicereceivedPayment = 0

    try:
        Invoicepending = Challan.objects.filter(current_status='NOT-PAID').count()
    except:
        Invoicepending = 0


    # =============================== Inventory Section ==========================
    try:
        Inventory_inStock = Inventory.objects.filter(current_status="IN-STOCK").count()
    except:
        Inventory_inStock = 0

    try:
        Inventory_sold_count = Inventory.objects.filter(current_status="OUT-OF-STOCK").count()
    except:
        Inventory_sold_count = 0


    # =============================== Production Section ==========================
    try:
        total_productionIn_a_Month = Production.objects.filter(created_at__month=current_month).count()
    except:
        total_productionIn_a_Month = 0

    try:
        due_production_in_a_month = Production.objects.filter(created_at__month=current_month, payment="NOT-PAID").count()
    except:
        due_production_in_a_month = 0


    # =============================== Top Sold Products Section ==========================
    try:
        topSoledProducts = Inventory.objects.filter(current_status="OUT-OF-STOCK").values("product__name", "product__id").annotate(sold_unites=Sum('production__quantity')).order_by('-sold_unites').first()
    except:
        topSoledProducts = {'product__name': 'NONE', 'product__id': 0, 'sold_unites': 0}


    data = {
        'employee': {
            'totalEmployee': total_employee,
            'activeEmployee': activeEmployee,
            'employeeOftheMonth': {
                'name': employee_of_the_month['employee__name'] if employee_of_the_month else "NONE",
                'id': employee_of_the_month['employee__id'] if employee_of_the_month else 0,
                'totalEarned': employee_of_the_month['total_payment'] if employee_of_the_month else 0,
                'producedUnites': producedUnites,
            },
            'topEmployees': [{
                'name': emp['employee__name'],
                'id': emp['employee__id']
            } for emp in top_employees],
        },
        'invoice': {
            'receivedPayment': InvoicereceivedPayment,
            'pending': Invoicepending,
            'total': total_invoice,
        },
        'inventory': {
            'inStock': Inventory_inStock,
            'sold': Inventory_sold_count,
            'total': total_inventory,
        },
        'totalCustomer': total_customers,
        'production': {
            'totalProduction': total_production,
            'totalProductionInAMounth': total_productionIn_a_Month,
            'due': due_production_in_a_month,
        },
        'products': {
            'totalProducts': total_products,
            'topSoledProducts': {
                'name': topSoledProducts['product__name'] if topSoledProducts else "NONE",
                'id': topSoledProducts['product__id'] if topSoledProducts else 0,
                'soldUnits': topSoledProducts['sold_unites'] if topSoledProducts else 0,
            },
        },
        'totalCategory': total_category,
    }

    return JsonResponse(data=data, safe=False, status=200)
