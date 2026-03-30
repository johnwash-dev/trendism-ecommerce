from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart, Wishlist,CartItem
from apps.products.models import Product, Size


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
        product_id = request.POST.get('product_id')
        size_id = request.POST.get('size_id')
    if not size_id:
        return JsonResponse({'status':'size_required'}, status=400)
    product = get_object_or_404(Product, id=product_id)
    size = get_object_or_404(Size, id=size_id)
    
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
    if not created:
        item.quantity += 1
        item.save()

    return JsonResponse({
            'status': 'success', 
            'cart_count': cart.items.count(),
            'message': 'Product added to cart!'
        })

def update_cart(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
        else:
            item.delete()
            return JsonResponse({'status':'removed'})
    item.save()
    return JsonResponse({'status':'success','quantity':item.quantity, 'sub_total':item.sub_total})


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('carts:cart:detail')

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


