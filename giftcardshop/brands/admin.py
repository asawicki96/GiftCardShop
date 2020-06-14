from django.contrib import admin
from .models import Brand, Category
from django import forms
from django.db import models
from .forms import BinaryFileInput



# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'active']
    list_filter = ['created']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_list', 'created', 'active', 'get_logo']
    list_filter = ['created', 'category']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    formfield_overrides = {
        models.BinaryField: {'widget': BinaryFileInput()},
    }

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('category')

    def category_list(self, obj):
        return ", ".join(o.name for o in obj.category.all())
