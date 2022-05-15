# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.landing, name='landing'),

    path('loading/', views.loading, name='loading'),
    path('index/', views.index, name='index'),
    path('createit/', views.branding, name='branding'),
    path('product/<int:id>', views.product, name='product'),
    path('feedback/', views.feedback, name='feedback'),
    path('all/categories', views.categories, name='categories'),
    path('categories/<int:pk>', views.product_by_category, name='product_by_category'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('product/all/', views.allproducts, name='allproducts'),
    path('checkout/buy/product/<int:id>/', views.checkout, name='checkout'),
    path('cases/', views.cases, name='cases'),
    path('logos/',views.view_logos, name='logos'),
    path('your/products/',views.myproducts, name='myproducts'),
    path('search/',views.search_product,name="search"),
    path('transaction/', views.transaction, name='transaction'),
    path('saveDesign/',views.save_design,name='save'),
    path('create-checkout-session/',views.create_checkout_session,name='create_checkout_session'),
    path('success/',views.notify_success,name='success'),
    path('cancelled/',views.notify_cancelled,name='cancelled'),
    path("config/",views.stripe_config, name='config'),
]