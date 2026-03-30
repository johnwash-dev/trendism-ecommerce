from django.shortcuts import render
from ..products.models import Category,Product, HomeBanners
from apps.carts.models import Wishlist

# Create your views here.
def homePage(request):
    user_wishlist_ids = []
    for p in Product.objects.all():
       p.save()

    if request.user.is_authenticated:
        user_wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

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
        'user_wishlist_ids': list(user_wishlist_ids),
    }

    return render(request, 'home.html', context)