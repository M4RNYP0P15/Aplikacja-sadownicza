from django.db import models
from .category import Category
from tinymce.models import HTMLField
from django.shortcuts import get_object_or_404
from django.db.models import Q
from itertools import chain

class Products(models.Model):
    name = models.CharField(max_length=70)
    price = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/')

    def get_cat_list(self):
        k = self.category
        breadcrumb = ['dummy']
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Products.objects.all()

    # @property
    # def children(self):
    #     return Products.objects.filter()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            kat = get_object_or_404(Category, id=category_id)
            all_kat = Category.objects.filter(parent=kat).reverse()
            all_prods = Products.objects.filter(category=category_id) | Products.objects.filter(category__in=all_kat)
            return all_prods
        else:
            return Products.get_all_products()