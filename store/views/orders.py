from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products
from store.models.orders import Order
from ..decorators import user_not_authenticated
# from store.middleware.auth import auth_middleware
from django.contrib.auth.decorators import login_required

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

@login_required
def my_order_view(request):
    customer=Customer.objects.get(id=request.user.id)
    orders=Order.objects.all().filter(customer_id = customer)
    ordered_products=[]
    for order in orders:
        ordered_product=Products.objects.all().filter(id=order.product.id)
        ordered_products.append(ordered_product)

    return render(request,'my_order.html',{'data':zip(ordered_products,orders)})

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return


def download_invoice_view(request,orderID,productID):
    order=Order.objects.get(id=orderID)
    product=Products.objects.get(id=productID)
    mydict={
        'orderDate':order.date,
        'customerName':request.user.get_name,
        'customerEmail':order.email,
        'customerMobile':order.phone,
        'shipmentAddress':order.address,
        'orderStatus':order.status.encode('utf-8'),

        'productName':product.name,
        'productImage':product.image,
        'productPrice':product.price,
        'productDescription':product.description,


    }
    return render_to_pdf('download_invoice.html',mydict)


# class OrderView(View):

#     def get(self, request):
#         customer = request.session.get('customer')
#         print(request.user)
#         orders = Order.get_orders_by_customer(customer)
#         print(orders)
#         return render(request , 'orders.html'  , {'orders' : orders})