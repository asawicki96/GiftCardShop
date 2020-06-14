from django.db import models
from taggit.managers import TaggableManager
from base64 import b64encode
from django.utils.safestring import mark_safe

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    description = models.CharField(max_length=1024, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['name'], name="category_name_idx"),
        ]
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256, unique=True)
    category = models.ManyToManyField(Category, verbose_name='categories')
    description = models.TextField(blank=True, null=True)
    logo = models.BinaryField(blank=True, null=True, editable=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    

    class Meta:
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['name'], name="brand_name_idx"),
        ]
        
    def __str__(self):
        return self.name

    def scheme_image_tag(self):
        return mark_safe('<img src = "data: image/png; base64, {}" width="200" height="100">'.format(
            b64encode(self.logo).decode()
        ))

    scheme_image_tag.short_description = 'Image'
    scheme_image_tag.allow_tags = True
    

