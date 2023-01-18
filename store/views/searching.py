from store.models.product import Products
from django.shortcuts import redirect, render

def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=Products.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Wyniki szukania:"

    if request.user.is_authenticated:
        return render(request,'customer_home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart, 'search_text': query})
    return render(request,'index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart, 'search_text': query})

def filter_data(request):
    query = request.GET['query']
    products=Products.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Wyniki szukania:"

    if request.user.is_authenticated:
        return render(request,'customer_home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart, 'search_text': query})
    return render(request,'index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart, 'search_text': query})
