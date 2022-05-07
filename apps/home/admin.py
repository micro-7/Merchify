# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    list_display = ('name','created')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''Admin View for Product'''

    list_display = ('name','description','price','color','dimension','created_on','category')
    search_fields = ('name',)

@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    '''Admin View for Logo'''

    list_display = ('user','image','created_on')
    search_fields = ('user',)

@admin.register(Custom_Design)
class Custom_DesignAdmin(admin.ModelAdmin):
    '''Admin View for Custom_Design'''

    list_display = ('user','created_on','product','design_image')
    search_fields = ('user',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Admin View for Order'''

    list_display = ('user','custom_design','quantity','price','created_on','order_complete')
    search_fields = ('user',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    '''Admin View for Transaction'''

    list_display = ('user','transaction_id','address','order_detail','is_complete','created_on','is_delivered','amount')
    search_fields = ('user','transaction_id',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    '''Admin View for Contact'''

    list_display = ('name','email','subject','message')
    search_fields = ('name',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    '''Admin View for Feedback'''

    list_display = ('name','phone','email','description',)

@admin.register(PlainProduct)
class PlainProductAdmin(admin.ModelAdmin):
    '''Admin View for PlainProduct'''

    list_display = ('name','description','price','color','dimension','created_on','category')
    search_fields = ('name',)
    
