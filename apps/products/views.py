import re
from django.shortcuts import render, get_object_or_404 
from .models import Product, Category
from django.db.models import Q



def product_list(request):
    products = Product.objects.all()

    cat_parameter = request.GET.get('category')
    gender = request.GET.get('gender')
    min_discount = request.GET.get('min_discount')
    q_search = request.GET.get('q')

    if cat_parameter:
        cat_slugs = cat_parameter.split(',')
        products = products.filter(category__slug__in=cat_slugs)

        for slug in cat_slugs:
            match = re.search(r'under-(\d+)', slug)
            if match:
                price_limit = int(match.group(1))
                products = products.filter(original_price__lte=price_limit)
    if gender:
        products = products.filter(gender__iexact=gender)
    
    if min_discount:
        products = products.filter(discount_percentage__gte=int(min_discount))

    if q_search:
        products = products.filter(Q(name__icontains=q_search) | Q(brand__icontains=q_search) | Q(color__icontains=q_search))
   
    return render(request, 'products/productList.html', {'products':products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    discount_percentage = 0
    if product.discount_price and product.discount_price > 0:
        savings = product.original_price - product.discount_price
        discount_percentage = round((savings / product.original_price) * 100)
    
    color_variants = []
    if product.style_group:
        color_variants = Product.objects.filter(style_group=product.style_group).exclude(id=product.id)
    
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:10]
    
    return render(request, 'detail.html', {
        'product': product,
        'related_products': related_products,
        'discount_percentage' : discount_percentage,
        'color_variants': color_variants
    })