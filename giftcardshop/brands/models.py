from django.db import models
from taggit.managers import TaggableManager

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=256, db_index=True, unique=True)
    slug = models.SlugField(max_length=256)
    description = models.TextField()
    #logo = models.models.ImageField(_(""), upload_to=None, height_field=None, width_field=None, max_length=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    tags = TaggableManager()
    

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = "Brands"
        
    def __str__(self):
        return self.name

    

