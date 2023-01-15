from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products
from store.models.orders import Order
from ..decorators import user_not_authenticated
# from store.middleware.auth import auth_middleware
from django.contrib.auth.decorators import login_required

@login_required
def my_order_view(request):
    customer=Customer.objects.get(id=request.user.id)
    orders=Order.objects.all().filter(customer_id = customer)
    ordered_products=[]
    for order in orders:
        ordered_product=Products.objects.all().filter(id=order.product.id)
        ordered_products.append(ordered_product)

    return render(request,'my_order.html',{'data':zip(ordered_products,orders)})

# class OrderView(View):

#     def get(self, request):
#         customer = request.session.get('customer')
#         print(request.user)
#         orders = Order.get_orders_by_customer(customer)
#         print(orders)
#         return render(request , 'orders.html'  , {'orders' : orders})