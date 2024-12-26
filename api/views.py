from .fractions.production_section import AddProduction, ViewProduction, UpdateProduction, DeleteProduction
from .fractions.cashmemo_section import CashMemoFilter, AddCashMemo, ViewAllCashmemo, SingleViewCashmemo
from .fractions.inventory_section import AddInventory, ViewInventory, UpdateInventory, DeleteInventory
from .fractions.employee_bill_section import AddEmployeeBill, ViewAllEmployeeBill, ViewEmployeeBill
from .fractions.employee_section import AddEmployee, ViewEmployee, UpdateEmployee, DeleteEmployee
from .fractions.customer_section import AddCustomer, ViewCustomer, UpdateCustomer, DeleteCustomer
from .fractions.products_section import AddProducts, ViewProducts, UpdateProducts, DeleteProducts
from .fractions.challan_section import AddChallan, ViewChallan, ViewAllChallan, DeleteChallan
from .fractions.catagory_section import AddCatagory, ViewCatagory, DeleteCatagory
from .fractions.employee_bill_filter_section import EmployeeBillFilter
from .fractions.filter_inventory_section import FilterInventory
from .fractions.simple_invoice_section import SimpleInvoice
from .fractions.dashboard_section import ViewDashboard
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


# ===================================== Challan Section =====================================
@csrf_exempt
def filter_inventory(request):
    data = FilterInventory(request=request)
    return data

@csrf_exempt
def add_challan(request):
    data = AddChallan(request=request)
    return data

def view_challan(request, pk):
    data = ViewAllChallan(request=request, pk=pk)
    return data

@csrf_exempt
def delete_challan(request):
    data = DeleteChallan(request=request)
    return data


def challan(request, pk):
    data = ViewChallan(request=request, pk=pk)
    return data

@csrf_exempt
def simple_invoice(request):
    data = SimpleInvoice(request)
    return data

# ===================================== Employee Bill Section =====================================
@csrf_exempt
def employee_bill_filter(request):
    data = EmployeeBillFilter(request=request)
    return data

@csrf_exempt
def add_employee_bill(request):
    data = AddEmployeeBill(request=request)
    return data


def view_employee_bill(request, pk):
    data = ViewAllEmployeeBill(request=request, pk=pk)
    return data

def view_single_employee_bill(request, pk):
    data = ViewEmployeeBill(request=request, pk=pk)
    return data


# ===================================== Cash Memo Section =====================================
def cash_memo_filter(request, pk):
    data = CashMemoFilter(request=request, pk=pk)
    return data

@csrf_exempt
def add_cash_memo(request):
    data = AddCashMemo(request=request)
    return data

def view_all_cashmemo(request, pk):
    data = ViewAllCashmemo(request=request, pk=pk)
    return data

@csrf_exempt
def view_single_memo(request, pk):
    data = SingleViewCashmemo(request=request, pk=pk)
    return data


# ===================================== Dashboard Section =====================================
def dashboard(request):
    data = ViewDashboard(request)
    return data
