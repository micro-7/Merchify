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
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from sympy import re
from .forms import *
from .models import *
import stripe
from django.shortcuts import render, redirect, get_object_or_404
import base64
from django.conf import settings
import time
from uuid import uuid4


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def save_checkout(request):
    for item in request.POST.items():
        print(f"{item}")
    name = request.POST.get('name')
    city = request.POST.get('city')
    
    address = request.POST.get('address')
    state = request.POST.get('state')
    country = request.POST.get('country')
    phone = request.POST.get('phone')
    zipcode = request.POST.get('zipcode')
    subject = request.POST.get('subject')
    email = request.POST.get('email')
    message = request.POST.get('message')
    c = Contact(name=name,city=city,address=address,state=state,country=country,phone=phone,zipcode=zipcode,subject=subject,email=email,message=message)
    c.save()
    return json.dumps({'success':'success'})

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = "http://127.0.0.1:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        price = request.GET.get('price')
        pid = request.GET.get('pid')
        item = Product.objects.filter(id=pid).first()

        price = str(price).replace('.', '0')
        print("price", price, "item", item)
        itemdata = [{
                    'name': item.name,
                    'quantity': 1,
                    'currency': 'inr',
                    'amount': int(price) * 100,
                    'description': item.description,
                    }]

        try:
            checkout_session = stripe.checkout.Session.create(
                # new
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + \
                'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=itemdata,
            )

            order = Transaction(
                user=request.user,
                transaction_id=checkout_session['id'],
                order_detail=item.name+" purchased",
                amount=price,
            )
            order.save()
            request.session['orderId'] = order.id
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})

@csrf_exempt
def create_custom_checkout_session(request):
    if request.method == 'GET':
        domain_url = "http://127.0.0.1:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        price = request.GET.get('price')
        pid = request.GET.get('pid')
        item = Custom_Design.objects.filter(id=pid).first()
        print(f'price {price}, id {pid}')
        print("price", price, "item", item)
        price = str(price).replace('.', '0')
        itemdata = [{
                    'name': item.product.name+"(custom)",
                    'quantity': 1,
                    'currency': 'inr',
                    'amount': int(price) * 100,
                    'description': item.product.description,
                    }]

        try:
            checkout_session = stripe.checkout.Session.create(
                # new
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + \
                'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=itemdata,
            )

            order = Transaction(
                user=request.user,
                transaction_id=checkout_session['id'],
                order_detail=item.product.name+" purchased",
                amount=price,
            )
            order.save()
            request.session['orderId'] = order.id
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})


def notify_success(request):
    messages.success(request, f"Your payment is complete.")
    if 'orderId' in request.session:
        order = Transaction.objects.get(id=request.session['orderId'])
        ctx = {'order': order}
        return render(request, "home/success.html", ctx)
    return render(request, "home/success.html")


def notify_cancelled(request):
    messages.error(request, f"Your payment is cancelled.")
    return render(request, "home/cancelled.html")


def loading(request):
    context = {'segment': 'loading'}

    html_template = loader.get_template('home/loading.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def feedback(request):
    context = {'segment': 'feedback'}
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            Contact = form.save(commit=False)
            Contact.user = request.user
            Contact.save()
            messages.success(request, 'Feedback successfully posted.')
            return redirect('landing')
        else:
            messages.error(request, 'Feedback could not be posted.')
    context['form'] = form
    html_template = loader.get_template('home/feedback.html')
    return render(request, 'home/feedback.html', context=context)


def landing(request):
    product = Product.objects.all()
    cate = Category.objects.all()[:4]
    ctx = {'title': "Home",
           'product': product,
           'cate': cate,
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
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            Contact = form.save(commit=False)
            Contact.user = request.user
            Contact.save()
            messages.success(request, 'Contact successfully posted.')
        else:
            messages.error(request, 'Contact could not be posted.')
    context['form'] = form
    product = get_object_or_404(Product, pk=id)
    context['product'] = product
    html_template = loader.get_template('home/checkout.html')
    return render(request, 'home/checkout.html', context=context)

@login_required(login_url="/login/")
def custom_checkout(request, id):
    context = {'segment': 'checkout'}
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            Contact = form.save(commit=False)
            Contact.user = request.user
            Contact.save()
            messages.success(request, 'Contact successfully posted.')
        else:
            messages.error(request, 'Contact could not be posted.')
    context['form'] = form
    product = get_object_or_404(Custom_Design, pk=id)
    context['c'] = product
    html_template = loader.get_template('home/checkout.html')
    return render(request, 'home/custom_checkout.html', context=context)

def product(request, id):
    context = {'segment': 'product'}
    product = get_object_or_404(Product, pk=id)
    context['product'] = product
    return render(request, 'home/product.html', context=context)

def custom_product(request, id):
    context = {'segment': 'custom design'}
    product = get_object_or_404(Custom_Design, pk=id)
    context['c'] = product
    return render(request, 'home/custom_product.html', context=context)


@login_required(login_url="/login/")
def dashboard(request):
    context = {'segment': 'dashboard'}
    form = LogoForm()
    if request.method == 'POST':
        form = LogoForm(request.POST, request.FILES)
        if form.is_valid():
            logo = form.save(commit=False)
            logo.user = request.user
            logo.save()
            messages.success(request, 'Logo successfully posted.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Logo could not be posted.')
    context['form'] = form
    html_template = loader.get_template('home/dashboard.html')
    return render(request, 'home/dashboard.html', context=context)


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


def product_by_category(request, pk):
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
        'products': products,
    }
    return render(request, 'home/branding.html', context=context)


@login_required(login_url="/login/")
def transaction(request):
    context = {'segment': 'transaction'}
    transactions = Transaction.objects.filter(user=request.user).all()
    context['transactions'] = transactions    
    return render(request,'home/transaction.html',context)


@csrf_exempt
@login_required(login_url='/login/')
def save_design(request):
    if request.is_ajax and request.method == "POST":

        product_id = request.POST['product']
        prd = get_object_or_404(PlainProduct, pk=int(product_id))
        desing_str = request.POST['design']
        format, imgstr = desing_str.split(';base64,')
        ext = 'png'
        data = ContentFile(base64.b64decode(imgstr))
        myfile = f"design/{prd.name}_{time.strftime('%Y%m%d')}." + ext
        print(myfile)
        fs = FileSystemStorage('media')
        filename = fs.save(myfile, data)
        # print(filename)
        m = Custom_Design(user=request.user, product=prd,
                          design_image=filename)
        m.save()
    return HttpResponse("done")

def search_product(request):
    q = request.GET.get('query')
    if q:
        results = Product.objects.filter(name__contains=q)
        print(results)
        if len(results)>0:
            ctx = {
                'title':'Search Results',
                'results':results,
                'query':q,
            }
            return render(request, "home/search.html",ctx)
    return redirect('landing')

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



