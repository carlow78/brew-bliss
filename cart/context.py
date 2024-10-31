from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):
    cart_items = []
    total = 0
    delivery = 0
    product_count = 0
    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    
    if request.path == '/checkout/': 
        if total < settings.FREE_DELIVERY_THRESHOLD:
            delivery = 3.95
        else:
            delivery = 0

    final_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'final_total': final_total,
    }

    return context