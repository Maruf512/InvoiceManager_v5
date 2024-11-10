from rest_framework import serializers
from .models import Catagory, Products, Employee, Production, Inventory, EmployeeBill, Customer, Challan, CashMemo


class CatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catagory
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'rate', 'catagory_id']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'address', 'nid_no', 'mobile']



class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = ['id', 'products_id', 'employee_id', 'quantity', 'rate']



class EmployeeBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeBill
        fields = '__all__'



class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'company_name', 'address', 'mobile']



class ChallanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challan
        fields = '__all__'



class CashMemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashMemo
        fields = '__all__'





