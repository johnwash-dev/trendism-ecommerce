from django.shortcuts import render
from ..products.models import Category,Product, HomeBanners

# Create your views here.
def homePage(request):

    for p in Product.objects.all():
       p.save()
    banners = HomeBanners.objects.filter(is_active=True)
    trending_categories = Category.objects.filter(is_trending=True).order_by('order')[:8]

    featured_product = Product.objects.filter(is_featured=True)[:8]
    return render(request, 'home.html', {'banners' : banners, 'featured_product' : featured_product, 'trending_categories':trending_categories})