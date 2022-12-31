from django import forms
from django.contrib.auth.models import User
from .models import category, customer, orders, product
from django.contrib.auth.forms import AuthenticationForm

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model=customer.Customer
        fields=['address','phone','profile_pic']


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