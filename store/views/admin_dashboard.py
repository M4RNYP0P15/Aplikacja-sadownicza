# from django.db import models
from ..models import customer, product, orders, category
from dictionary.models import article
# from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from ..decorators import user_is_superuser, user_is_moderator
from .. import forms
from django.contrib import messages
import json
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
# from django.utils.translation import ugettext as _

def is_leap_year(year): 
    if year % 100 == 0:
        return year % 100 == 0

    return year % 4 == 0

def get_lapse(date):
    last_month = date.month
    current_year = date.year

    if last_month in [9, 4, 6, 11]:
        lapse = 30

    elif last_month in [1, 3, 5, 7, 8, 10, 12]:
        lapse = 31
    else:
        if is_leap_year(current_year):
            lapse = 29
        else:
            lapse = 30

    return lapse

from django.db.models.functions import TruncMonth
# @login_required(login_url='adminlogin')
@user_is_moderator
def admin_dashboard_view(request):
    customercount=customer.Customer.objects.all().count()
    productcount=product.Products.objects.all().count()
    ordercount=orders.Order.objects.all().count()
    articlescount=article.Article.objects.all().count()

    _orders=orders.Order.objects.all()
    labelschart = ['']*12
    datachart =[0]*12
    f_date = datetime.today() # dzisiejsza data
    last_month_filter = f_date - timedelta(days=f_date.day, hours=f_date.hour, minutes=f_date.minute)
    # s_date = timedelta(days=get_lapse(f_date)) # ilość dni
    
    for i in reversed(range(12)):
        # print("od")
        # print(f_date)
        # print(last_month_filter)
        # print(f_date.strftime('%b'))
        labelschart[i]=f_date.strftime('%b')
        last_year_orders = orders.Order.objects.filter(date__gte=last_month_filter, date__lte=f_date)
        sum = 0
        for item in last_year_orders:
            sum += item.price
        datachart[i] = sum
        f_date = last_month_filter
        last_month_filter = f_date - timedelta(days=get_lapse(f_date))
        # s_date = timedelta(days=get_lapse(f_date))
    # datachart = [0, 10000, 5000, 15000, 10000, 20000, 15000, 25000, 20000, 30000, 25000, 35000]

    # print(datachart)
    # print(labelschart)

    ordered_products=[]
    ordered_bys=[]
    for order in _orders:
        ordered_product=product.Products.objects.all().filter(id=order.product.id)
        ordered_by=customer.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    mydict={
    'customercount':customercount,
    'productcount':productcount,
    'ordercount':ordercount,
    'articlescount':articlescount,
    'datachart': mark_safe(json.dumps(datachart)),
    'labelschart': mark_safe(json.dumps(labelschart)),
    'data':zip(ordered_products,ordered_bys,_orders),
    }
    return render(request,'admin/admin_dashboard.html',context=mydict)

@user_is_moderator
def view_customer_view(request):
    customers=customer.Customer.objects.all()
    return render(request,'admin/view_customer.html',{'customers':customers})

@user_is_superuser
def delete_customer_view(request,pk):
    _customer=customer.Customer.objects.get(id=pk)
    _customer.delete()
    return redirect('store:view-customer')

@user_is_superuser
def update_customer_view(request,pk):
    _customer=customer.Customer.objects.get(id=pk)
    if request.method=='POST':
        form=forms.CustomerUserForm(request.POST,instance=_customer)
        # customerForm=forms.CustomerForm(request.POST,instance=_customer)
        if form.is_valid():
            form.save()
            # user.set_password(user.password)
            # user.save()
            # customerForm.save()
            return redirect('store:view-customer')
    # user=User.objects.get(id=_customer.user_id)
    form=forms.CustomerUserForm(instance=_customer)
    # customerForm=forms.CustomerForm(request.FILES,instance=_customer)
    
    return render(request,'admin/admin_update_customer.html',context={'form':form})

@user_is_moderator
def admin_products_view(request):
    products=product.Products.objects.all()
    return render(request,'admin/admin_products.html',{'products':products})

@user_is_moderator
def admin_add_product_view(request):
    productForm=forms.ProductForm()
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        else:
            for error in list(productForm.errors.values()):
                messages.error(request, error)
        return HttpResponseRedirect('admin-products')
    return render(request,'admin/admin_add_products.html',{'productForm':productForm})


# @login_required(login_url='adminlogin')
@user_is_superuser
def delete_product_view(request,pk):
    _product=product.Products.objects.get(id=pk)
    _product.delete()
    return redirect('store:admin-products')


# @login_required(login_url='adminlogin')
@user_is_superuser
def update_product_view(request,pk):
    _product=product.Products.objects.get(id=pk)
    productForm=forms.ProductForm(instance=_product)
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST,request.FILES,instance=_product)
        if productForm.is_valid():
            productForm.save()
            return redirect('store:admin-products')
    return render(request,'admin/admin_update_product.html',{'productForm':productForm})


# @login_required(login_url='adminlogin')
@user_is_moderator
def admin_view_booking_view(request):
    _orders=orders.Order.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in _orders:
        ordered_product=product.Products.objects.all().filter(id=order.product.id)
        ordered_by=customer.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)
    return render(request,'admin/admin_view_booking.html',{'data':zip(ordered_products,ordered_bys,_orders)})


# @login_required(login_url='adminlogin')
@user_is_superuser
def delete_order_view(request,pk):
    order=orders.Order.objects.get(id=pk)
    order.delete()
    return redirect('store:admin-view-booking')

@user_is_moderator
def update_order_view(request,pk):
    order=orders.Order.objects.get(id=pk)
    orderForm=forms.OrderForm(instance=order)
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('store:admin-view-booking')
    return render(request,'admin/admin_update_order.html',{'form':orderForm})


# @login_required(login_url='adminlogin')
# def view_feedback_view(request):
#     feedbacks=models.Feedback.objects.all().order_by('-id')
#     return render(request,'admin/view_feedback.html',{'feedbacks':feedbacks})


@user_is_superuser
def admin_add_category(request):
    categoryForm = forms.AddCategory()
    if request.method=='POST':
        categoryForm=forms.AddCategory(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
        else:
            for error in list(categoryForm.errors.values()):
                messages.error(request, error)
        return HttpResponseRedirect('store:admin-add-category')
    return render(request,'admin/admin_add_category.html',{'categoryForm':categoryForm})

@user_is_moderator
def admin_category_view(request):
    elements=category.Category.objects.all()
    return render(request,'admin/admin_view_categories.html',{'elements':elements})

@user_is_superuser
def update_category_view(request,pk):
    _category=category.Category.objects.get(id=pk)
    if request.method=='POST':
        form=forms.AddCategory(request.POST, instance=_category)
        if form.is_valid():
            form.save()
            return redirect('store:admin-view-category')

    form=forms.AddCategory(instance=_category)
    return render(request,'admin/admin_update_category.html',context={'form':form})

@user_is_superuser
def delete_category_view(request,pk):
    _category=category.Category.objects.get(id=pk)
    _category.delete()
    return redirect('store:admin-view-category')
