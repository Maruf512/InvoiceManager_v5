from django.urls import path
from .views import add_employees, view_employees, update_employee, delete_employee, add_customer, view_all_customer, update_customer, delete_customer, add_catagory, view_catagory, delete_catagory, add_products, view_all_products, update_products, delete_products

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
    
    
    # Customer Routing
    path('customer/create/', add_customer, name="add_customer"),
    path('customer/view/<int:pk>/', view_all_customer, name="view_all_customer"),
    path('customer/update/<int:pk>/', update_customer, name="update_customer"),
    path('customer/delete/<int:pk>/', delete_customer, name="delete_customer"),



]

