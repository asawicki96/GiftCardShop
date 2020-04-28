from django.db import models
from taggit.managers import TaggableManager

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='brands/logo/%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    tags = TaggableManager()
    

    class Meta:
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['name'], name="brand_name_idx"),
        ]
        
    def __str__(self):
        return self.name

    

