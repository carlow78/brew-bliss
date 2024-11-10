from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
from products.models import Product
from django.http import HttpResponseRedirect


def view_cart(request):
    """ A view that renders the cart contents page """

    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

   
    if item_id in list(cart.keys()):
            cart[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {item_id}')
    else:
            cart[item_id] = quantity
            messages.success(request, f'Successfully added {product.name} to your cart!')

    request.session['cart'] = cart
    return redirect(redirect_url)


def modify_cart(request, item_id):
    """Adjust the quantity of the specified product in the cart"""

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id] = quantity
        messages.success(request, f"Updated quantity of {product.name} to {quantity}")
    else:
        item = cart.pop(item_id, None) 
        if item:
            messages.success(request, f"Removed item {cart[item_id]} from your cart")
        else:
            messages.info(request, f"Item {cart[item_id]} was not in your cart")

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):

    # Remove from cart - this function remove all quantities of an item from cart

    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        del cart[str(item_id)]
        request.session['cart'] = cart
    return redirect('view_cart')