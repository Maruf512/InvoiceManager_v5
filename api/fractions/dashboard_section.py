from django.shortcuts import render
from django.db.models import Sum
from ..models import EmployeeBill, Production, Employee, Challan, Product, Category, Inventory
from datetime import datetime
from django.db.models import F

def ViewDashboard(request):
    # Employee of the Month - Highest paid employee
    employee_of_the_month = EmployeeBill.objects.values('employee__name').annotate(
        total_payment=Sum('total_amount')).order_by('-total_payment').first()

    # Recent Productions (last 5)
    recent_productions = Production.objects.select_related('product').order_by('-created_at')[:5]

    # Recent Employee Bills (last 5)
    recent_employee_bills = EmployeeBill.objects.select_related('employee').order_by('-created_at')[:5]

    # Recent Challans (last 5)
    recent_challans = Challan.objects.select_related('customer').order_by('-created_at')[:5]

    # Total Sales Report - Total sales by product (last month)
    current_month = datetime.now().month
    last_month_sales = Production.objects.filter(
        created_at__month=current_month
    ).values('product__name').annotate(
        total_sales=Sum('quantity')
    ).order_by('-total_sales')

    # Categories Count
    categories_count = Category.objects.count()

    # Products Count
    products_count = Product.objects.count()

    # Employees Count
    employees_count = Employee.objects.count()

    # Inventory in stock and sold
    in_stock = Inventory.objects.filter(current_status="IN-STOCK").count()
    sold_count = Inventory.objects.filter(current_status="OUT-OF-STOCK").count()

    print({
        'employee_of_the_month': {'name': 'employee name', 'paid': 12000}

    })


    return render(request, 'dashboard.html', {
        'employee_of_the_month': employee_of_the_month,
        'recent_productions': recent_productions,
        'recent_employee_bills': recent_employee_bills,
        'recent_challans': recent_challans,
        'last_month_sales': last_month_sales,
        'categories_count': categories_count,
        'products_count': products_count,
        'employees_count': employees_count,
        'in_stock': in_stock,
        'sold_count': sold_count
    })
