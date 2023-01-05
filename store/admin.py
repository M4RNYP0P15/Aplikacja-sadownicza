from django.contrib import admin

#from .models import *
from .models.category import Category
from .models.product import Products
from .models.customer import Customer
from .models.orders import Order
# Register your models here.

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Customer)
admin.site.register(Products, AdminProduct)
# admin.site.register(User)
admin.site.register(Category)

admin.site.register(Order)
