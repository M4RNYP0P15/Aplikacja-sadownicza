import os
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('profile_pic', slugify(self.slug), instance)
        return None
    
    STATUS = (
        ('klient', 'klient'),
        ('moderator', 'moderator'),
        ('administrator', 'administrator'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='klient')
    profile_pic = models.ImageField(default='profile_pic/avatar.png',upload_to=image_upload_to, max_length=255)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=50)
    
    @property
    def get_name(self):
        return self.first_name+" "+ self.last_name

    @property
    def get_id(self):
        return self.id

    def __str__(self):
        return self.first_name

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