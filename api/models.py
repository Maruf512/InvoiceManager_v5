# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Catagory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'catagory'


class Products(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    rate = models.IntegerField()
    catagory = models.ForeignKey(Catagory, models.DO_NOTHING)
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
    products = models.ForeignKey('Products', models.DO_NOTHING)
    employee = models.ForeignKey(Employee, models.DO_NOTHING)
    quantity = models.IntegerField()
    rate = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'production'


class Inventory(models.Model):
    employee = models.OneToOneField(Employee, models.DO_NOTHING, primary_key=True)  # The composite primary key (employee_id, production_id) found, that is not supported. The first column is selected.
    products = models.ForeignKey('Products', models.DO_NOTHING)
    production = models.ForeignKey('Production', models.DO_NOTHING)
    current_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'inventory'
        unique_together = (('employee', 'production'),)


class EmployeeBill(models.Model):
    employee = models.OneToOneField(Employee, models.DO_NOTHING, primary_key=True)  # The composite primary key (employee_id, production_id) found, that is not supported. The first column is selected.
    production = models.ForeignKey('Production', models.DO_NOTHING)
    total_amount = models.IntegerField()
    current_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'employee_bill'
        unique_together = (('employee', 'production'),)


class Customer(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'customer'


class Challan(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)  # The composite primary key (id, employee_id, production_id) found, that is not supported. The first column is selected.
    customer = models.ForeignKey('Customer', models.DO_NOTHING)
    products = models.ForeignKey('Products', models.DO_NOTHING)
    employee = models.ForeignKey('Employee', models.DO_NOTHING)
    production = models.ForeignKey('Production', models.DO_NOTHING)
    current_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'challan'
        unique_together = (('id', 'employee', 'production'),)


class CashMemo(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)  # The composite primary key (id, products_id, customer_id, challan_id) found, that is not supported. The first column is selected.
    products = models.ForeignKey('Products', models.DO_NOTHING)
    customer = models.ForeignKey('Customer', models.DO_NOTHING)
    challan = models.ForeignKey('Challan', models.DO_NOTHING)
    total_yds = models.BigIntegerField()
    total_amount = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'cash_memo'
        unique_together = (('id', 'products', 'customer', 'challan'),)


