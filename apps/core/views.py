from django.shortcuts import render
from ..products.models import Category,Product, HomeBanners

# Create your views here.
def homePage(request):
    

    for p in Product.objects.all():
       p.save()
    banners = HomeBanners.objects.filter(is_active=True)
    trending_categories = Category.objects.filter(is_trending=True).order_by('order')[:8]

    top_deals = Category.objects.filter(top_deals=True)[:10]

    eid_banner = HomeBanners.objects.filter(title__icontains='Eid', is_active=False).first()

    featured_product = Product.objects.filter(is_featured=True)[:8]
    context ={
        'banners' : banners,
        'featured_product' : featured_product,
        'trending_categories' : trending_categories,
        'top_deals' : top_deals,
        'eid_banner' : eid_banner,
    }

    return render(request, 'home.html', context)