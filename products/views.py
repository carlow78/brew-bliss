from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product


def all_products(request):
    # show all products and search function

    products = Product.objects.all()
    query = request.GET.get('q', '')

    if request.GET:
        if query:
            search_fields = ['name', 'description']
            search_query = Q()

            for field in search_fields:
                search_query |= Q(**{f"{field}__icontains": query})

            products = products.filter(search_query)
        else:
            messages.error(request, "Please enter a search term.")
            return redirect(reverse('products'))

    context = {
        'products': products,
        'search_term': query
    }


    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)