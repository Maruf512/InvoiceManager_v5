from .fractions.production_section import AddProduction, ViewProduction, UpdateProduction, DeleteProduction
from .fractions.inventory_section import AddInventory, ViewInventory, UpdateInventory, DeleteInventory
from .fractions.employee_section import AddEmployee, ViewEmployee, UpdateEmployee, DeleteEmployee
from .fractions.customer_section import AddCustomer, ViewCustomer, UpdateCustomer, DeleteCustomer
from .fractions.products_section import AddProducts, ViewProducts, UpdateProducts, DeleteProducts
from .fractions.catagory_section import AddCatagory, ViewCatagory, DeleteCatagory
from .fractions.challan_section import AddChallan, ViewChallan, ViewAllChallan
from .fractions.filter_inventory_section import FilterInventory
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


# ====================== Employee Section =====================
@csrf_exempt
def add_employees(request):
    data = AddEmployee(request=request)
    return data


def view_employees(request, pk):
    data = ViewEmployee(request=request, pk=pk)
    return data


@api_view(['PUT'])
def update_employee(request, pk):
    data = UpdateEmployee(request=request, pk=pk)
    return data


def delete_employee(request, pk):
    data = DeleteEmployee(request=request, pk=pk)
    return data


# ====================== Customer Section =====================
@csrf_exempt
def add_customer(request):
    data = AddCustomer(request=request)
    return data


def view_all_customer(request, pk):
    data = ViewCustomer(request=request, pk=pk)
    return data


@api_view(['PUT'])
def update_customer(request, pk):
    data = UpdateCustomer(request=request, pk=pk)
    return data


def delete_customer(request, pk):
    data = DeleteCustomer(request=request, pk=pk)
    return data


# ====================== Catagory Section =====================
@csrf_exempt
def add_catagory(request):
    data = AddCatagory(request=request)
    return data


def view_catagory(request):
    data = ViewCatagory(request=request)
    return data


def delete_catagory(request, pk):
    data = DeleteCatagory(request=request, pk=pk)
    return data


# ====================== Products Section =====================
@csrf_exempt
def add_products(request):
    data = AddProducts(request=request)
    return data


def view_all_products(request, pk):
    data = ViewProducts(request=request, pk=pk)
    return data


@api_view(['PUT'])
def update_products(request, pk):
    data = UpdateProducts(request=request, pk=pk)
    return data


def delete_products(request, pk):
    data = DeleteProducts(request=request, pk=pk)
    return data



# ====================== Production Section =====================
@csrf_exempt
def add_production(request):
    data = AddProduction(request=request)
    return data


def view_all_production(request, pk):
    data = ViewProduction(request=request, pk=pk)
    return data


@api_view(['PUT'])
def update_production(request, pk):
    data = UpdateProduction(request=request, pk=pk)
    return data


def delete_production(request, pk):
    data = DeleteProduction(request=request, pk=pk)
    return data


# ====================== Inventory Section =====================
@csrf_exempt
def add_inventory(request):
    data = AddInventory(request=request)
    return data


def view_inventory(request, pk):
    data = ViewInventory(request=request, pk=pk)
    return data


@api_view(['PUT'])
def update_inventory(request, pk):
    data = UpdateInventory(request=request, pk= pk)
    return data


def delete_inventory(request, pk):
    data = DeleteInventory(request=request, pk=pk)
    return data


# ===================================== Filter Inventory Section =====================================
@csrf_exempt
def filter_inventory(request):
    data = FilterInventory(request=request)
    return data


# ===================================== Challan Section =====================================
@csrf_exempt
def add_challan(request):
    data = AddChallan(request=request)
    return data


def view_challan(request, pk):
    data = ViewAllChallan(request=request, pk=pk)
    return data

def challan(request, pk):
    data = ViewChallan(request=request, pk=pk)
    return data


# ===================================== Employee Bill Section =====================================

