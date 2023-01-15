from django import forms
# from django.contrib.auth.models import User
from .models import category, customer, orders, product
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, PasswordChangeForm, PasswordResetForm, UserCreationForm
from django.contrib.auth import get_user_model

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nazwa użytkownika/Email'}),
        label="Nazwa użytkownika lub Email")

    password = forms.CharField(
        widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Hasło'}),
        label="Hasło")
    
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'profile_pic']

# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model=customer.Customer
#         fields=['address','phone','profile_pic']

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = customer.Customer
        fields=[
            'first_name',
            'last_name',
            'username', 
            'profile_pic', 
            'address',
            'phone'
            ]

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='Wprowadz adres email.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user

class ProductForm(forms.ModelForm):
    class Meta:
        model=product.Products
        fields=['name','price','description','image']

#address of shipment
class AddressForm(forms.Form):
    Email = forms.EmailField()
    Mobile= forms.IntegerField()
    Address = forms.CharField(max_length=500)

# class FeedbackForm(forms.ModelForm):
#     class Meta:
#         model=Feedback
#         fields=['name','feedback']

class OrderForm(forms.ModelForm):
    class Meta:
        model=orders.Order
        fields=['status']

#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))