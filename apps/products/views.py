from django.shortcuts import render, get_object_or_404 
from .models import Product, Category


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'productList.html', {'category' : category, 'products' : products})

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