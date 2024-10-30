from django.shortcuts import render

def view_cart(request):
    # View for shopping cart
    
    return render(request, 'cart/cart.html')
