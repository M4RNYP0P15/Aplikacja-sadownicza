from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from store.models.customer import Customer
from django.views import View
from store import forms

def customer_signup_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            login(request, user)
            messages.success(request, f"Uworzono nowe konto: {user.username}")
            return HttpResponseRedirect('logged')
        else:
            for error in list(userForm.errors.values() )+ list(customerForm.errors.values()):
                messages.error(request, error)

    return render(request,'signup.html',context=mydict)

# class Signup (View):
# 	def get(self, request):
# 		return render(request, 'signup.html')

# 	def post(self, request):
# 		postData = request.POST
# 		first_name = postData.get('firstname')
# 		last_name = postData.get('lastname')
# 		phone = postData.get('phone')
# 		email = postData.get('email')
# 		password = postData.get('password')
# 		# validation
# 		value = {
# 			'first_name': first_name,
# 			'last_name': last_name,
# 			'phone': phone,
# 			'email': email
# 		}
# 		error_message = None

# 		customer = Customer(first_name=first_name,
# 							last_name=last_name,
# 							phone=phone,
# 							email=email,
# 							password=password)
# 		error_message = self.validateCustomer(customer)

# 		if not error_message:
# 			print(first_name, last_name, phone, email, password)
# 			customer.password = make_password(customer.password)
# 			customer.register()
# 			return redirect('homepage')
# 		else:
# 			data = {
# 				'error': error_message,
# 				'values': value
# 			}
# 			return render(request, 'signup.html', data)

# 	def validateCustomer(self, customer):
# 		error_message = None
# 		if (not customer.first_name):
# 			error_message = "Proszę wprowadzić imię!"
# 		elif len(customer.first_name) < 3:
# 			error_message = 'Imię musi składać się z co najmniej 3 znaków'
# 		elif not customer.last_name:
# 			error_message = 'Proszę wprowadzić nazwisko'
# 		elif len(customer.last_name) < 3:
# 			error_message = 'Nazwisko musi składać się z co najmniej 3 znaków'
# 		elif not customer.phone:
# 			error_message = 'Proszę wprowadzić numer telefonu'
# 		elif len(customer.phone) < 10:
# 			error_message = 'Numer telefonu musi składać się z co najmniej 10 znaków'
# 		elif len(customer.password) < 5:
# 			error_message = 'Hasło musi składać się z co najmniej 5 znaków'
# 		elif len(customer.email) < 5:
# 			error_message = 'Email musi składać się z co najmniej 5 znaków'
# 		elif customer.isExists():
# 			error_message = 'Konto o podanym adresie e-mail już istnieje'
# 		# saving

# 		return error_message
