from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from ..forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages

# def is_customer(user):
#     return user.groups.filter(name='CUSTOMER').exists()


def afterlogin_view(request):
    if request.user.is_superuser:
        return redirect('store:admin-dashboard')
    else:
        return redirect('store:homepage')

@login_required
def custom_logout(request):
	# request.session.clear()
	logout(request)
	messages.info(request, "Zostałeś pomyślnie wylogowany!")
	return redirect('store:homepage')

def custom_login(request):
	if request.user.is_authenticated:
		return redirect('store:homepage')

	if request.method == 'POST':
		# form = AuthenticationForm(request=request, data=request.POST)
		form = UserLoginForm(request=request, data=request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data['username'],
								password=form.cleaned_data['password'],
			)
			if user is not None:
				login(request, user)
				# request.session['customer'] = user.id
				messages.success(request, f"Witaj <b>{user.username}</b>! Pomyślnie zalogowano!")
				return redirect('store:homepage')
		else:
			for key, error in list(form.errors.items()):
				if key == 'captcha' and error[0] == 'To pole jest wymagane.':
					messages.error(request, "Musisz wykonać test reCAPTCHA.")
					continue
				messages.error(request, error)

	# form = AuthenticationForm()
	form = UserLoginForm()
	return render(request=request, template_name="login.html", context={'form': form})

### usunac
class Login(View):
	return_url = None

	def get(self, request):
		Login.return_url = request.GET.get('return_url')
		return render(request, 'login.html')

	def post(self, request):
		email = request.POST.get('email')
		password = request.POST.get('password')
		customer = Customer.get_customer_by_email(email)
		error_message = None
		if customer:
			flag = check_password(password, customer.password)
			if flag:
				request.session['customer'] = customer.id

				if Login.return_url:
					return HttpResponseRedirect(Login.return_url)
				else:
					Login.return_url = None
					return redirect('homepage')
			else:
				error_message = 'Nie poprawne dane logowania!'
		else:
			error_message = 'Użytkownik o podanym adresie email nie istnieje!'

		print(email, password)
		return render(request, 'login.html', {'error': error_message})


def logout(request):
	request.session.clear()
	return redirect('store:login')
