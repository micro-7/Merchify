# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import json
from unicodedata import category
from django.contrib import messages
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from sympy import re
from .forms import *
from .models import *
from django.shortcuts import render, redirect,get_object_or_404
import base64
import time



@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

def loading(request):
    context = {'segment': 'loading'}

    html_template = loader.get_template('home/loading.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def feedback(request):
    context = {'segment': 'feedback'}
    form = FeedbackForm()
    if request.method=='POST':
        form  = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            Contact = form.save(commit=False)
            Contact.user = request.user
            Contact.save()
            messages.success(request,'Feedback successfully posted.')
            return redirect('landing')
        else:
            messages.error(request,'Feedback could not be posted.')
    context['form'] = form
    html_template = loader.get_template('home/feedback.html')
    return render(request,'home/feedback.html',context = context)

def landing(request):
    product = Product.objects.all()
    cate = Category.objects.all()[:4]
    ctx = {'title': "Home",
           'product': product,
           'cate' : cate,
           }
    return render(request, "home/landing.html", ctx)

def myproducts(request):
    product = Custom_Design.objects.filter(user=request.user)
    ctx = {'title': "Home",
           'product': product,
           }
    return render(request, "home/myproducts.html", ctx)

def cases(request):
    product = Product.objects.all()
    ctx = {'title': "Home",
           'product': product,
           }
    return render(request, "home/cases.html", ctx)

def allproducts(request):
    allproduct = Product.objects.all()
    ctx = {'title': "All Products",
           'allproduct': allproduct,
           }
    return render(request, "home/allproducts.html", ctx)


@login_required(login_url="/login/")
def checkout(request, id):
    context = {'segment': 'checkout'}
    form = ContactForm()
    if request.method=='POST':
        form  = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            Contact = form.save(commit=False)
            Contact.user = request.user
            Contact.save()
            messages.success(request,'Contact successfully posted.')
            return redirect('transaction')
        else:
            messages.error(request,'Contact could not be posted.')
    context['form'] = form
    product = get_object_or_404(Product,pk=id)
    context['product'] = product
    html_template = loader.get_template('home/checkout.html')
    return render(request,'home/checkout.html',context = context)


def product(request,id):
    context = {'segment': 'product'}
    product = get_object_or_404(Product,pk=id)
    context['product'] = product
    return render(request, 'home/product.html',context=context)
    
@login_required(login_url="/login/")
def dashboard(request):
    context = {'segment': 'dashboard'}
    form = LogoForm()
    if request.method=='POST':
        form  = LogoForm(request.POST, request.FILES)
        if form.is_valid():
            logo = form.save(commit=False)
            logo.user = request.user
            logo.save()
            messages.success(request,'Logo successfully posted.')
            return redirect('dashboard')
        else:
            messages.error(request,'Logo could not be posted.')
    context['form'] = form
    html_template = loader.get_template('home/dashboard.html')
    return render(request,'home/dashboard.html',context = context)

@login_required(login_url="/login/")
def view_logos(request):
    logo = Logo.objects.all()
    ctx = {'title': "All Logos",
           'logo': logo,
           }
        
    return render(request, "home/logos.html", ctx)

def categories(request):
    categories = Category.objects.all()
    ctx = {'title': "All Catagories",
           'categories': categories,
           }
    return render(request, "home/categories.html", ctx)

def product_by_category(request,pk):
    products = Product.objects.filter(category__id=pk)
    ctx = {'title': "All Catagories",
           'products': products,
           }
    return render(request, "home/categorybased.html", ctx)

@login_required(login_url="/login/")
def branding(request):
    logos = Logo.objects.filter(user=request.user)
    products = PlainProduct.objects.all()

    context = {
        'segment': 'branding',
        'logos': logos,
        'products':products,
        }
    return render(request,'home/branding.html',context=context)

@login_required(login_url="/login/")
def transaction(request):
    context = {'segment': 'transaction'}

    html_template = loader.get_template('home/transaction.html')
    return HttpResponse(html_template.render(context, request))

@csrf_exempt
@login_required(login_url='/login/')
def save_design(request):
    if request.is_ajax and request.method == "POST":
        
        product_id = request.POST['product']
        prd = get_object_or_404(PlainProduct,pk=int(product_id))
        desing_str = request.POST['design']
        format, imgstr = desing_str.split(';base64,')
        ext = 'png'
        data = ContentFile(base64.b64decode(imgstr))
        myfile = f"design/{prd.name}_{time.strftime('%Y%m%d')}." + ext
        print(myfile)
        fs = FileSystemStorage('media')
        filename = fs.save(myfile, data)
        # print(filename)
        m = Custom_Design(user=request.user,product=prd,design_image=filename)
        m.save()
    return HttpResponse("done")

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


# C:\Users\mihir\projects\Merchify\media\design\Black Plain_20220508.png
# C:\Users\mihir\projects\Merchify\core\media\design\Black Plain_20220508.png