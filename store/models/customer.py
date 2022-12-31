import os
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Customer(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('profile_pic', slugify(self.slug), instance)
        return None
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='profile_pic/avatar.png',upload_to=image_upload_to, max_length=255)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=40)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+ self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
    
    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        
        return False