from rest_framework import serializers
from .models import Category, Product, Employee, Production, Inventory, EmployeeBill, Customer, Challan, CashMemo


class CatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'rate', 'category']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'address', 'nid_no', 'mobile']



class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = ['id', 'product', 'employee', 'quantity', 'rate']



class EmployeeBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeBill
        fields = '__all__'



class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['employee', 'product', 'production', 'current_status']



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





