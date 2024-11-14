from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    # show all products view, Plus search and sort queries.
    
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    sortkey = None
  

    if request.GET:

        sortkey = request.GET.get('sort', 'name')
        direction = request.GET.get('direction', 'asc')

        if sortkey == 'name':
            sortkey = 'lower_name'
            products = products.annotate(lower_name=Lower('name'))

        if direction == 'desc':
            sortkey = f'-{sortkey}'

        products = products.order_by(sortkey)
       
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q'].strip()
            if not query:
                messages.error(request, "Search criteria is missing. Please enter search term.")
                return redirect (reverse('products'))
                
                queries = Q(name__icontains=query) | Q(description__icontains=query)
                products = products.filter(queries).distinct()

    current_sorting = f'{sortkey}_{direction}'

    context = {
        'products':products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }


    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    #A view to show individual product details

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):

     if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product to the store')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please check your form for issues')
     else:
        form = ProductForm()
        
        template = 'products/add_product.html'
        context = {
        'form': form,
    }

     return render(request, template, context)


@login_required
def edit_product(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please check form for errors.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    # Delete product from store

        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        messages.success(request, 'Product removed from store!')
        return redirect(reverse('products'))