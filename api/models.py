from django.db import models


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, default='yds')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'catagory'


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    rate = models.IntegerField()
    production_cost = models.FloatField(db_column='production_cost')
    other_cost = models.FloatField(default=0, db_column='other_cost')
    category = models.ForeignKey(Category, models.RESTRICT, db_column='catagory_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'products'


class Employee(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    nid_no = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'employee'


class Production(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, models.CASCADE, db_column='products_id')
    employee = models.ForeignKey(Employee, models.CASCADE)
    quantity = models.FloatField()
    rate = models.FloatField()
    payment = models.CharField(max_length=50, default='NOT-PAID')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'production'


class Inventory(models.Model):
    id = models.BigAutoField(primary_key=True)
    employee = models.ForeignKey(Employee, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE, db_column='products_id')
    production = models.ForeignKey(Production, models.CASCADE)
    current_status = models.CharField(max_length=50, default='IN-STOCK')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'inventory'


class EmployeeBill(models.Model):
    id = models.BigAutoField(primary_key=True)
    employee = models.ForeignKey(Employee, models.CASCADE, db_column='employee_id')
    total_amount = models.FloatField()
    current_status = models.CharField(max_length=50, default='NOT-PAID')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'employee_bill'


class EmployeeBillProduction(models.Model):
    employee_bill_id = models.ForeignKey(EmployeeBill, on_delete=models.CASCADE, db_column='employee_bill_id')
    product = models.ForeignKey(Product, models.CASCADE, db_column='products_id')
    production = models.ForeignKey(Production, on_delete=models.CASCADE, db_column='production_id')
    rate = models.FloatField()
    quantity = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employee_bill_production'  # Specify the table name explicitly
        managed = False  # Disable Django's management of this table




class Customer(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, default='NONE')
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default='NONE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'customer'


class Challan(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(Customer, models.CASCADE)
    total = models.CharField(max_length=100)
    current_status = models.CharField(max_length=50, default='NOT-PAID')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'challan'


# Junction table to connect Production to Challan
class ChallanProduction(models.Model):
    challan = models.ForeignKey(Challan, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, models.CASCADE, db_column='employee_id')
    product = models.ForeignKey(Product, models.CASCADE, db_column='products_id')
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'challan_production'  # Specify the table name explicitly
        managed = False  # Disable Django's management of this table



class CashMemo(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(Customer, models.CASCADE)
    total_yds = models.BigIntegerField()
    total_amount = models.BigIntegerField()

    discount = models.FloatField(max_length=100, default=0)
    total_after_discount = models.FloatField(max_length=100, default=0)
    discount_method = models.CharField(max_length=20, default='%')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'cash_memo'


class CashMemoChallan(models.Model):
    cashmemo = models.ForeignKey(CashMemo, on_delete=models.CASCADE, db_column='cash_memo_id')
    product = models.ForeignKey(Product, models.CASCADE, db_column='products_id')
    challan = models.ForeignKey(Challan, on_delete=models.CASCADE, db_column='challan_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cashmemo_Challan'
        managed = False
