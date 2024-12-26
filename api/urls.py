from django.urls import path
from .views import *

urlpatterns = [
    # Dashboard Routing
    path('dashboard/', dashboard, name="Dashboard"),

    # Catagory Routing
    path('catagory/create/', add_catagory, name="add_catagory"),
    path('catagory/view/', view_catagory, name="view_catagory"),
    path('catagory/delete/<int:pk>/', delete_catagory, name="delete_catagory"),

    # Products Routing
    path('products/create/', add_products, name="add_products"),
    path('products/view/<int:pk>/', view_all_products, name="view_all_products"),
    path('products/update/<int:pk>/', update_products, name="update_products"),
    path('products/delete/<int:pk>/', delete_products, name="delete_products"),

    # Employee Routing
    path('employee/create/', add_employees, name="Add Employees"),
    path('employee/view/<int:pk>/', view_employees, name="view_all_employee"),
    path('employee/update/<int:pk>/', update_employee, name="update_employee"),
    path('employee/delete/<int:pk>/', delete_employee, name="delete_employee"),

    # Production Routing
    path('production/create/', add_production, name="add_production"),
    path('production/view/<int:pk>/', view_all_production, name="view_all_production"),
    path('production/update/<int:pk>/', update_production, name="Update Production"),
    path('production/delete/<int:pk>/', delete_production, name="delete_products"),
    
    # Inventory Routing
    path('inventory/add/', add_inventory, name="add production to inventory"),
    path('inventory/view/<int:pk>/', view_inventory, name="view_inventory"),
    path('inventory/update/<int:pk>/', update_inventory, name="Update Inventory"),
    path('inventory/delete/<int:pk>/', delete_inventory, name="delete inventory"),

    # Customer Routing
    path('customer/create/', add_customer, name="add_customer"),
    path('customer/view/<int:pk>/', view_all_customer, name="view_all_customer"),
    path('customer/update/<int:pk>/', update_customer, name="update_customer"),
    path('customer/delete/<int:pk>/', delete_customer, name="delete_customer"),

    # Challan Routing
    path('challan/<int:pk>/', challan, name="View Single Challan"),
    path('challan/create/', add_challan, name="add_challan"),
    path('challan/view/<int:pk>/', view_challan, name="View Challan"),
    path('challan/delete/', delete_challan, name="Delete Challan"),
    # Simple Invoice Section
    path('invoice/create/', simple_invoice, name="Create Simple Invoice"),
    # Filter
    # get data from inventory for challan
    path('inventory/filter/', filter_inventory, name="Get Inventory by Employee"),

    # Employee Bill Routing
    path('employee/bill/filter/', employee_bill_filter, name="Employee Filter Section"),
    path('employee/bill/create/', add_employee_bill, name="Create Employee Bill"),
    path('employee/bill/view/<int:pk>/', view_employee_bill, name="View All Employee Bill"),
    path('employee/bill/single/view/<int:pk>/', view_single_employee_bill, name="View Single Employee Bill"),

    # Cash Memo Routing
    path('memo/create/', add_cash_memo, name="Create CashMemo"),
    path('memo/view/<int:pk>/', view_all_cashmemo, name="View All Cash Memo"),
    path('memo/filter/<int:pk>/', cash_memo_filter, name="Filter Invoice For CashMemo"),
    path('memo/single/view/<int:pk>/', view_single_memo, name="View Single Memo"),
]

