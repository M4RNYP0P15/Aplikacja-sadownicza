from django.db import models
from django.utils import timezone
from store.models import category
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model

from django.template.defaultfilters import slugify
import os

class Article(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join("Artykuly", slugify(self.category.slug), slugify(self.slug), instance)
        return None

    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)
    slug = models.SlugField("article", null=False, blank=False, unique=True)
    content = HTMLField(blank=True, default="")
    publish_date = models.DateTimeField("Data publikacji", default=timezone.now)
    modified_date = models.DateTimeField("Data modyfikacji", default=timezone.now)
    category = models.ForeignKey(category.Category, default="", verbose_name="category", on_delete=models.SET_DEFAULT)
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    image = models.ImageField(default='default/no_image.jpg', upload_to=image_upload_to, max_length=255)

    def __str__(self):
        return self.title

    def get_cat_list(self):
        k = self.category
        breadcrumb = ['dummy']
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]

    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    # @property
    # def slug(self):
    #     return self.category.slug + "/" + self.slug

    class Meta:
        verbose_name_plural = "articles"
        ordering = ['-publish_date']