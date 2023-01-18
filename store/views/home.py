from django.shortcuts import render, redirect, HttpResponseRedirect
from store.models.product import Products
from store.models.category import Category
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# class Index(View):

# 	def post(self, request):
# 		return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')
# 		# product = request.POST.get('product')
# 		# remove = request.POST.get('remove')
# 		# cart = request.session.get('cart')
# 		# if cart:
# 		# 	quantity = cart.get(product)
# 		# 	if quantity:
# 		# 		if remove:
# 		# 			if quantity <= 1:
# 		# 				cart.pop(product)
# 		# 			else:
# 		# 				cart[product] = quantity-1
# 		# 		else:
# 		# 			cart[product] = quantity+1

# 		# 	else:
# 		# 		cart[product] = 1
# 		# else:
# 		# 	cart = {}
# 		# 	cart[product] = 1

# 		# request.session['cart'] = cart
# 		# print('cart', request.session['cart'])
# 		# return redirect('store:homepage')

# 	def get(self, request):
# 		# print()
# 		return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')


def home_view(request):
	cart = request.session.get('cart')
	if not cart:
		request.session['cart'] = {}
	products = None
	# categories = Category.get_all_categories()
	categories = Category.objects.all()
	categoryID = request.GET.get('category')
	if categoryID:
		products = Products.get_all_products_by_categoryid(categoryID)
	else:
		products = Products.get_all_products()

	data = {}
	data['products'] = products
	data['categories'] = categories

	print('email : ', request.session.get('email'))
	return render(request, 'index.html', data)


def customer_home_view(request):
    products=Products.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    return render(request,'customer_home.html',{'products':products,'product_count_in_cart':product_count_in_cart})


def store(request):
	products = None
	categories = Category.objects.all()
	temp_hierarch = []
	categoryID = request.GET.get('category')
	if categoryID:
		products = Products.get_all_products_by_categoryid(categoryID).order_by('-price')
		category_hierarch = Category.objects.filter(pk=categoryID).first()
		temp_hierarch.append(category_hierarch)
		while category_hierarch.parent != None:
			# print(category_hierarch.parent.pk)
			category_hierarch = Category.objects.filter(pk=category_hierarch.parent.pk).first()
			temp_hierarch.insert(0,category_hierarch)
		
		# for element in temp_hierarch:
		# 	print(element)
	else:
		products = Products.get_all_products().order_by('-price')
	
	if 'product_ids' in request.COOKIES:
		product_ids = request.COOKIES['product_ids']
		counter=product_ids.split('|')
		product_count_in_cart=len(set(counter))
	else:
		product_count_in_cart=0
	
	page_num = request.GET.get('page')
	paginator = Paginator(products, 2)
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
	return render(request,'index.html',{'data':data,'product_count_in_cart':product_count_in_cart})