from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key':'pk_test_51Q19bS01JENvyaBElkBKg3TubIzVzqQ5cy0zrAubqt0CcIDAwSGcVGORe3gqeeqfblK2Hu8yYA29dss8xbEhfVfk00aJ7ZeonS',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)