from django.shortcuts import render
from django.views import View
from braces.views import LoginRequiredMixin
from .models import Brand, Category
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .forms import SearchForm
# Create your views here.


class BrandListView(View):
    def get(self, request, category='all'):
        form = SearchForm()
        query = None

        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                cleanedData = form.cleaned_data
                query = cleanedData['query']
                brands = Brand.objects.filter(name__icontains=query)
        else:
            brands = Brand.objects.all()

        categories = Category.objects.all().order_by('name')
        
        page = request.GET.get('page', None)

        if category != 'all':
            brands = brands.filter(category__slug=category)

        paginator = Paginator(brands, 12)
        page_obj = paginator.get_page(page)

        context = {
            'page_obj': page_obj,
            'categories': categories,
            'category': category,
            'form': form,
            'query': query
        }
        
        return render(request, 'brands/list.html', context)

class BrandDetailView(View):
    def get(self, request, slug):
        brand = get_object_or_404(Brand, slug=slug)
        categories = Category.objects.filter(brand=brand)

        context = {
            'brand': brand,
            'categories': categories
        }

        return render(request, 'brands/detail.html', context)
        