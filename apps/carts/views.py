import json
from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart, Wishlist,CartItem
from apps.products.models import Product, Size,Variations


def cart_detail_page(request):
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).prefetch_related('items__product').first()
    return render(request, 'carts/cart_detail.html', {'cart':cart})

def wishList_page(request):
    wishlist_items=[]

    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')

    return render(request, 'carts/wishList_page.html', {'wishlist_items':wishlist_items})

def add_to_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status':'login_required'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            variation_id = int(data.get('size_id'))

            if not variation_id:
                return JsonResponse({'status':'error', 'message':'Please select the size'}, status=400)
            
            

            variations = get_object_or_404(Variations, id=variation_id, product_id=product_id)

            product = variations.product
            size = variations.size

            if variations.stock <= 0:
                return JsonResponse({'status':'error', 'message':f'Sorry, size {variations.size.name} is currently out of stock!'}, status=200)
            
            cart, _ = Cart.objects.get_or_create(user=request.user)

            item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
            if created:
                item.quantity = 1  
            else:
                item.quantity += 1 
            item.save()

            cart_count = CartItem.objects.filter(cart__user=request.user).count()

            return JsonResponse({
                'status': 'success', 
                'cart_count': cart_count,
                'message': 'Product added to cart Successfully!'
               })
        except Exception as e:
            return JsonResponse({'status':'error','message':str(e)}, status=400)
    return JsonResponse({'status':'error', 'message':'Invalid request'}, status=400)

    

def update_cart(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
        else:
            item.delete()
            return JsonResponse({
                'status': 'removed',
                'cart_total': item.cart.total_amount,
                'total_mrp': item.cart.total_mrp,
                'total_discount': item.cart.total_discount,
                'cart_count': item.cart.items.count()
            })
            
    item.save()
    return JsonResponse({
        'status': 'success',
        'quantity': item.quantity,
        'original_price_total': item.total_original_price, 
        'cart_count': item.cart.items.count(),
        'sub_total': item.sub_total,
        'cart_total': item.cart.total_amount,
        'total_mrp': item.cart.total_mrp,
        'total_discount': item.cart.total_discount
    })

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart = item.cart
    item.delete()
    
    # AJAX request-ah check pandrom
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'removed',
            'cart_count': cart.items.count(),
            'total_mrp': cart.total_mrp,
            'total_discount': cart.total_discount,
            'cart_total': cart.total_amount
        })
        
    return redirect('carts:cart_detail')

def toggle_wishlist(request, product_id): 
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'login_required'}, status=401)
    
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

        if not created:
            wishlist_item.delete()
            return JsonResponse({'status': 'removed'})
        
        return JsonResponse({'status': 'added'})
    
    return JsonResponse({'status': 'invalid_request'}, status=400)


