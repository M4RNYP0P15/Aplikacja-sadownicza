from store.models.product import Products
from store.models.category import Category

from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# def search_view(request):
#     # whatever user write in search box we get in query
#     query = request.GET['query']
#     products=Products.objects.all().filter(name__icontains=query)
#     if 'product_ids' in request.COOKIES:
#         product_ids = request.COOKIES['product_ids']
#         counter=product_ids.split('|')
#         product_count_in_cart=len(set(counter))
#     else:
#         product_count_in_cart=0

#     return render(request,'index.html',{'products':products,'product_count_in_cart':product_count_in_cart, 'search_text': query})

def search_view(request):
	products = None
	categories = Category.objects.all()
	temp_hierarch = []
	categoryID = request.GET.get('category')
	query = request.GET['query']
	print(query)
	# products=Products.objects.all().filter(name__icontains=query)
	if categoryID:
		products = Products.get_all_products_by_categoryid(categoryID).order_by('-price')
		products = products.filter(name__icontains=query)
		category_hierarch = Category.objects.filter(pk=categoryID).first()
		temp_hierarch.append(category_hierarch)
		while category_hierarch.parent != None:
			category_hierarch = Category.objects.filter(pk=category_hierarch.parent.pk).first()
			temp_hierarch.insert(0,category_hierarch)
	else:
		products = Products.get_all_products().order_by('-price')
		products = products.filter(name__icontains=query)
	
	if 'product_ids' in request.COOKIES:
		product_ids = request.COOKIES['product_ids']
		counter=product_ids.split('|')
		product_count_in_cart=len(set(counter))
	else:
		product_count_in_cart=0
	
	page_num = request.GET.get('page')
	paginator = Paginator(products, 10)
	try:
		page_obj = paginator.page(page_num)
	except PageNotAnInteger:
		page_obj = paginator.page(1)
	except EmptyPage:
		page_obj = paginator.page(paginator.num_pages)

	data = {}
	data['page_obj'] = page_obj
	data['categories'] = categories
	data['cur_category'] = categoryID
	data['hist_category'] = temp_hierarch
	return render(request,'index.html',{'data':data,'product_count_in_cart':product_count_in_cart, 'search_text': query})

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

    return render(request,'index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart, 'search_text': query})
