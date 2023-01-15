# from django.db import models
from ..models import customer, product, orders
# from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from ..decorators import user_is_superuser
from .. import forms


# @login_required(login_url='adminlogin')
@user_is_superuser
def admin_dashboard_view(request):
    customercount=customer.Customer.objects.all().count()
    productcount=product.Products.objects.all().count()
    ordercount=orders.Order.objects.all().count()

    _orders=orders.Order.objects.all()
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
    'data':zip(ordered_products,ordered_bys,_orders),
    }
    return render(request,'admin/admin_dashboard.html',context=mydict)

# login_required(login_url='adminlogin')
@user_is_superuser
def view_customer_view(request):
    customers=customer.Customer.objects.all()
    return render(request,'admin/view_customer.html',{'customers':customers})

# @login_required(login_url='adminlogin')
@user_is_superuser
def delete_customer_view(request,pk):
    _customer=customer.Customer.objects.get(id=pk)
    _customer.delete()
    return redirect('store:view-customer')


# @login_required(login_url='adminlogin')
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

# admin view the product
# @login_required(login_url='adminlogin')
@user_is_superuser
def admin_products_view(request):
    products=product.Products.objects.all()
    return render(request,'admin/admin_products.html',{'products':products})


# admin add product by clicking on floating button
# @login_required(login_url='adminlogin')
@user_is_superuser
def admin_add_product_view(request):
    productForm=forms.ProductForm()
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-products')
    return render(request,'admin/admin_add_products.html',{'productForm':productForm})


# @login_required(login_url='adminlogin')
@user_is_superuser
def delete_product_view(request,pk):
    _product=product.Products.objects.get(id=pk)
    _product.delete()
    return redirect('admin-products')


# @login_required(login_url='adminlogin')
@user_is_superuser
def update_product_view(request,pk):
    _product=product.Products.objects.get(id=pk)
    productForm=forms.ProductForm(instance=_product)
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST,request.FILES,instance=_product)
        if productForm.is_valid():
            productForm.save()
            return redirect('admin-products')
    return render(request,'admin/admin_update_product.html',{'productForm':productForm})


# @login_required(login_url='adminlogin')
@user_is_superuser
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
    return redirect('admin-view-booking')

# for changing status of order (pending,delivered...)
# @login_required(login_url='adminlogin')
@user_is_superuser
def update_order_view(request,pk):
    order=orders.Order.objects.get(id=pk)
    orderForm=forms.OrderForm(instance=order)
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request,'admin/update_order.html',{'orderForm':orderForm})


# @login_required(login_url='adminlogin')
# def view_feedback_view(request):
#     feedbacks=models.Feedback.objects.all().order_by('-id')
#     return render(request,'admin/view_feedback.html',{'feedbacks':feedbacks})
