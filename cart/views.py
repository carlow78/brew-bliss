from django.shortcuts import render, redirect

def view_cart(request):
    # View for shopping cart
    
    return render(request, 'cart/cart.html')

def add_to_cart(request, item_id):

    # View to control quantity of an item in cart

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    weight = None
    if 'product_weight' in request.POST:
        weight = request.POST['product_weight']

    cart = request.session.get('cart', {})

    if weight:
        if item_id in list(cart.keys()):
            if weight in cart[item_id]['items_by_weight'].keys():
                cart[item_id]['items_by_weight'][weight] += quantity
            else:
                cart[item_id]['items_by_weight'][weight] = quantity
        else:
            cart[item_id] = {'items_by_weight': {weight: quantity}}
    else:
        if item_id in list(cart.keys()):
            cart[item_id] += quantity
        else:
            cart[item_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)

