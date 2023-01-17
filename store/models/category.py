from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=230, default='', blank=True)
    slug = models.SlugField("category", null=False, blank=False, unique=True)
    publish_date = models.DateTimeField('Data publikacji', default=timezone.now)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_DEFAULT, default=None)

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name_plural = "categories"
        ordering = ['-publish_date']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '->'.join(full_path[::-1])

    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)



# class Category(models.Model):
#     name = models.CharField(max_length=50)

#     @staticmethod
#     def get_all_categories():
#         return Category.objects.all()
    
#     def __str__(self):
#         return self.name