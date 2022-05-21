# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from pyexpat import model
from tkinter import PhotoImage
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="category")
    created = models.DateTimeField(auto_now=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'

    def __str__(self):
        """Unicode representation of Category."""
        return self.name

class Product(models.Model):  
    name = models.CharField(max_length=225)
    image = models.ImageField(upload_to="product")
    description = models.TextField()
    price = models.CharField(max_length=225) 
    color = models.CharField(max_length=225) 
    dimension = models.CharField(max_length=150)
    created_on = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Product."""
        return self.name

class PlainProduct(models.Model):  
    name = models.CharField(max_length=225)
    image = models.ImageField(upload_to="plainproduct")
    description = models.TextField()
    price = models.CharField(max_length=225) 
    color = models.CharField(max_length=225) 
    dimension = models.CharField(max_length=150)
    created_on = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)

    # TODO: Define fields here

    class Meta:
        """Meta definition for PlainProduct."""

        verbose_name = 'PlainProduct'
        verbose_name_plural = 'PlainProducts'

    def __str__(self):
        """Unicode representation of PlainProduct."""
        return self.name

class Logo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="logo")
    created_on = models.DateTimeField(auto_now=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Logo."""

        verbose_name = 'Logo'
        verbose_name_plural = 'Logos'

    def __str__(self):
        """Unicode representation of Logo."""
        return self.image.url

class Custom_Design(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    design_image = models.ImageField(upload_to="design")
    product = models.ForeignKey(PlainProduct,on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Custom_Design'
        verbose_name_plural = 'Custom_Designs'

    def __str__(self):
        """Unicode representation of Custom_Design."""
        return self.product.name

class Order(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    custom_design = models.ForeignKey(Custom_Design,on_delete=models.DO_NOTHING)
    quantity = models.IntegerField() 
    price = models.FloatField() 
    created_on = models.DateTimeField(auto_now=True)
    order_complete = models.BooleanField(default=False)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Order."""

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        """Unicode representation of Order."""
        return self.user

class Transaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=50)
    order_detail = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    amount = models.FloatField() 

    # TODO: Define fields here

    class Meta:
        """Meta definition for Transaction."""

        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        """Unicode representation of Transaction."""
        return f"{self.amount}"
        
class Contact(models.Model):
    name = models.CharField(max_length=225)
    address = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    state = models.CharField(max_length=225)
    country = models.CharField(max_length=225)
    phone = models.CharField(max_length=225)
    zipcode = models.CharField(max_length=225)
    subject = models.CharField(max_length=225)
    email = models.EmailField()
    message = models.CharField(max_length=225)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Contact."""

        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        """Unicode representation of Contact."""
        return self.name

class Feedback(models.Model):
    name = models.CharField(max_length=225)
    phone = models.CharField(max_length=225)
    email = models.EmailField()
    description = models.TextField()

    # TODO: Define fields here

    class Meta:
        """Meta definition for Feedback."""

        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def __str__(self):
        """Unicode representation of Feedback."""
        return self.name
