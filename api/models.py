from django.db import models


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'catagory'


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    rate = models.IntegerField()
    category = models.ForeignKey(
        Category,
        models.RESTRICT,
        db_column='catagory_id'
    )
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
    product = models.ForeignKey(Product, models.RESTRICT, db_column='products_id')
    employee = models.ForeignKey(Employee, models.RESTRICT)
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
    employee = models.ForeignKey(Employee, models.RESTRICT)
    product = models.ForeignKey(Product, models.RESTRICT, db_column='products_id')
    production = models.ForeignKey(Production, models.RESTRICT)
    current_status = models.CharField(max_length=50, default='IN-STOCK')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'inventory'


class EmployeeBill(models.Model):
    id = models.BigAutoField(primary_key=True)
    employee = models.ForeignKey(Employee, models.RESTRICT)
    production = models.ForeignKey(Production, models.RESTRICT)
    total_amount = models.IntegerField()
    current_status = models.CharField(max_length=50, default='NOT-PAID')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'employee_bill'


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
    customer = models.ForeignKey(Customer, models.RESTRICT)
    total = models.CharField(max_length=100)
    current_status = models.CharField(max_length=50, default='NOT-PAID')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'challan'


# Junction table to connect Production to Challan
class ChallanProduction(models.Model):
    challan = models.ForeignKey(Challan, on_delete=models.RESTRICT)
    employee = models.ForeignKey(Employee, models.RESTRICT, db_column='employee_id')
    product = models.ForeignKey(Product, models.RESTRICT, db_column='products_id')
    production = models.ForeignKey(Production, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'challan_production'  # Specify the table name explicitly
        managed = False  # Disable Django's management of this table



class CashMemo(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, models.RESTRICT, db_column='products_id')
    customer = models.ForeignKey(Customer, models.RESTRICT)
    challan = models.ForeignKey(Challan, models.RESTRICT)
    total_yds = models.BigIntegerField()
    total_amount = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'cash_memo'
