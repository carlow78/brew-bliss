from django.conf import settings


def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total + (settings.STANDARD_DELIVERY)
        free_delivery_target = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_target = 0

    
    final_total = delivery + total


    context = {

        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_target': free_delivery_target,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'final_total': final_total,

    }

    return context
