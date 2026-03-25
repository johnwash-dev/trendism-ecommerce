import re
from django.shortcuts import render, get_object_or_404 
from .models import Product, Category, Color
from django.db.models import Q
from django.db.models.functions import Coalesce



def product_list(request):
    products = Product.objects.annotate(
        effective_price=Coalesce('discount_price', 'original_price')
    )

    cat_parameter = request.GET.get('category')
    gender_parameter = request.GET.get('gender')
    brand_parameter = request.GET.get('brand')
    color_parameter = request.GET.get('color')
    price_range = request.GET.get('price')
    sort_by = request.GET.get('sort','newest')
    min_discount = request.GET.get('min_discount')
    q_search = request.GET.get('q')

    show_categories = True
    if cat_parameter:
        # Gen Z logic 
        if gender_parameter and gender_parameter.lower() == 'gen z':
            show_categories = True
        else:
            show_categories = False

        cat_slugs = cat_parameter.split(',')
        
        # 1. Start with an empty Q object to collect conditions
        final_category_query = Q()
        price_limit_query = Q()

        for slug in cat_slugs:
            # Price Extraction (e.g., shirts-under-499)
            price_match = re.search(r'(\d+)', slug)
            if price_match:
                price_limit = int(price_match.group(1))
                price_limit_query |= Q(effective_price__lte=price_limit)
            
            # Category Name Extraction
            category_part = slug.split('-under-')[0]
            
            if category_part:
                # T-Shirt logic: Strict match
                if 't-shirt' in category_part or 'tshirt' in category_part:
                    final_category_query |= (
                        Q(category__slug__icontains='t-shirt') | 
                        Q(category__name__icontains='t-shirt') |
                        Q(category__name__icontains='tshirt')
                    )
                # Shirt logic: Exclude T-shirts specifically
                elif 'shirt' in category_part:
                    final_category_query |= (
                        Q(category__slug__icontains='shirt') | 
                        Q(category__name__icontains='shirt')
                    ) & ~Q(category__name__icontains='t-shirt') & ~Q(category__slug__icontains='t-shirt')
                
                # Others
                else:
                    clean_name = category_part.replace('-', ' ')
                    final_category_query |= (
                        Q(category__name__icontains=clean_name) | 
                        Q(category__slug__icontains=category_part) |
                        Q(category__parent__name__icontains=clean_name)
                    )

        if final_category_query:
            products = products.filter(final_category_query)
        if price_limit_query:
            products = products.filter(price_limit_query)

    if gender_parameter:
        if gender_parameter.lower() != 'gen z':
            products = products.filter(
                Q(category__name__iexact=gender_parameter) | 
                Q(category__parent__name__iexact=gender_parameter) |
                Q(category__parent__parent__name__iexact=gender_parameter)
            )
    
    if price_range:
        try:
            low, high = price_range.split('-')
            products = products.filter(effective_price__range=(float(low), float(high)))
        except (ValueError, TypeError):
            pass

    if brand_parameter:
        brand_list = brand_parameter.split(',')
        products = products.filter(brand__in=brand_list)

    if color_parameter:
        color_list = color_parameter.split(',')
        products = products.filter(color__color_name__in=color_list)
    
    if min_discount:
        products = products.filter(discount_percentage__gte=int(min_discount))

    if q_search:
        search_words = q_search.split()
        combined_query = Q()

        for word in search_words:
            combined_query &= (
                Q(name__icontains=word) | 
                Q(brand__icontains=word) | 
                Q(color__color_name__icontains=word) | 
                Q(category__name__icontains=word)
            )
        
        products = products.filter(combined_query).distinct()
    
    if sort_by == 'price_low':
        products = products.order_by('effective_price')
    elif sort_by == 'price_high':
        products = products.order_by('-effective_price')
    else:
        products = products.order_by('-id')

   

    available_brands = products.values_list('brand', flat=True).distinct().order_by('brand')
    sub_categories = []
    if gender_parameter and gender_parameter.lower() != 'gen z':
        sub_categories = Category.objects.filter(parent__name__iexact=gender_parameter)
    
    all_sub_categories = Category.objects.exclude(parent=None).exclude(parent__name__iexact='Gen Z')

    all_colors = Color.objects.filter(product__in=products).distinct()

    #AJAX logic
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        for p in products:
            if p.discount_price and p.original_price > 0:
               p.discount_percentage = round(((p.original_price - p.discount_price) / p.original_price) * 100)
            else:
               p.discount_percentage = 0
        return render(request, 'products/includes/product_grid.html', {'products': products.distinct()})

    context = {
        'products': products.distinct(),
        'sort_by': sort_by,
        'show_categories': show_categories,
        'brands_preview': available_brands[:10], 
        'brands_more': available_brands[10:], 
        'colors_preview': all_colors[:10],      
        'colors_more': all_colors[10:],         
        'sub_categories': sub_categories[:10],  
        'all_sub_categories': all_sub_categories,
    }
   
    return render(request, 'products/productList.html', context)

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
    
    return render(request, 'products/detail.html', {
        'product': product,
        'related_products': related_products,
        'discount_percentage' : discount_percentage,
        'color_variants': color_variants
    })