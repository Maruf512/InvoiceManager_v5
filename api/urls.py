from django.urls import path
from .views import add_employees, view_employees, update_employee, delete_employee, add_customer, view_all_customer, update_customer, delete_customer, add_catagory, view_catagory, delete_catagory, add_products, view_all_products, update_products, delete_products, add_production, view_all_production, update_production, delete_production, add_inventory, view_inventory, update_inventory, delete_inventory, filter_inventory

urlpatterns = [
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
    

    # Inventory Section
    path('inventory/add/', add_inventory, name="add production to inventory"),
    path('inventory/view/<int:pk>/', view_inventory, name="view_inventory"),
    path('inventory/update/<int:pk>/', update_inventory, name="Update Inventory"),
    path('inventory/delete/<int:pk>/', delete_inventory, name="delete inventory"),



    # Customer Routing
    path('customer/create/', add_customer, name="add_customer"),
    path('customer/view/<int:pk>/', view_all_customer, name="view_all_customer"),
    path('customer/update/<int:pk>/', update_customer, name="update_customer"),
    path('customer/delete/<int:pk>/', delete_customer, name="delete_customer"),


    # Filter
    # get data from inventory by employee
    path('inventory/filter/', filter_inventory, name="Get Inventory by Employee"),






]

