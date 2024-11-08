from django.urls import path
from .views import add_employees, view_employees, update_employee, delete_employee, add_customer, view_all_customer, update_customer, delete_customer, add_catagory

urlpatterns = [
    # Catagory Routing
    path('catagory/create/', add_catagory, name="add_catagory"),


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

