from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category


def all_products(request):
    # show all products view, Plus search and sort queries.
    
    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
       
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q'].strip()
            if query:
                queries = Q(name__icontains=query) | Q(description__icontains=query)
                products = products.filter(queries).distinct()
            else:
                messages.error(request, "Search criteria is missing. Please enter search term.")


    context = {
        'products':products,
        'search_term': query,
        'current_categories': categories,
    }


    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)