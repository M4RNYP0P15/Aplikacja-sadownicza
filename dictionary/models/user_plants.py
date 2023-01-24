from django.db import models
from django.utils import timezone
from store.models import category, customer
from dictionary.models import article
from django.contrib.auth import get_user_model

from django.template.defaultfilters import slugify

class UserPlant(models.Model):
    user = models.ForeignKey(customer.Customer, on_delete=models.CASCADE, related_name="user_plants")
    item = models.ForeignKey(article.Article, on_delete=models.CASCADE)
    slug = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.item.title