from django_filters import FilterSet, RangeFilter
from .models import product

class ProductFilter(FilterSet):
    price = RangeFilter()
    
    class Meta:
        model = product.Products
        fields = ['price']
