# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import timezone


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
    quantity = models.FloatField()
    rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'production'



class Inventory(models.Model):
    # Auto-incrementing primary key ID
    id = models.BigAutoField(primary_key=True)

    # Foreign key relationships with specified database column names
    employee = models.ForeignKey('Employee', models.DO_NOTHING, db_column='employee_id')
    products = models.ForeignKey('Products', models.DO_NOTHING, db_column='products_id')
    production = models.ForeignKey('Production', models.DO_NOTHING, db_column='production_id')

    # Current status field with default value 'IN-STOCK'
    current_status = models.CharField(max_length=50, default='IN-STOCK')

    # Timestamps with default and auto-update behavior
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False  # Do not let Django manage schema changes
        db_table = 'inventory'  # Use existing table name



class EmployeeBill(models.Model):
    # Auto-incrementing primary key ID
    id = models.BigAutoField(primary_key=True)

    # Foreign key relationships with specified database column names
    employee = models.ForeignKey('Employee', models.DO_NOTHING, db_column='employee_id')
    production = models.ForeignKey('Production', models.DO_NOTHING, db_column='production_id')

    # Total amount and current status fields
    total_amount = models.IntegerField()  # Matches SQL INT type
    current_status = models.CharField(max_length=50, default='NOT-PAID')

    # Timestamps with default and auto-update behavior
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False  # Do not let Django manage the schema for this table
        db_table = 'employee_bill'  # Use the existing database table name


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
    # Auto-incrementing primary key ID
    id = models.BigAutoField(primary_key=True)

    # Foreign key relationships with specified database column names
    customer = models.ForeignKey('Customer', models.DO_NOTHING, db_column='customer_id')
    products = models.ForeignKey('Products', models.DO_NOTHING, db_column='products_id')
    employee = models.ForeignKey('Employee', models.DO_NOTHING, db_column='employee_id')
    production = models.ForeignKey('Production', models.DO_NOTHING, db_column='production_id')

    # Current status field with default value 'NOT-PAID'
    current_status = models.CharField(max_length=50, default='NOT-PAID')

    # Timestamps with default and auto-update behavior
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False  # Do not let Django manage the schema for this table
        db_table = 'challan'  # Use the existing database table name


class CashMemo(models.Model):
    # Auto-incrementing primary key ID
    id = models.BigAutoField(primary_key=True)

    # Foreign key relationships with specified database column names
    products = models.ForeignKey('Products', models.DO_NOTHING, db_column='products_id')
    customer = models.ForeignKey('Customer', models.DO_NOTHING, db_column='customer_id')
    challan = models.ForeignKey('Challan', models.DO_NOTHING, db_column='challan_id')

    # Fields for total yards and total amount
    total_yds = models.BigIntegerField()  # Matches SQL BIGINT type
    total_amount = models.BigIntegerField()  # Matches SQL BIGINT type

    # Timestamps with default and auto-update behavior
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False  # Prevent Django from managing the schema for this table
        db_table = 'cash_memo'  # Use the existing database table name


