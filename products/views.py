from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category, Wishlist, Review
from .forms import ProductForm, ReviewForm
import logging

logger = logging.getLogger(__name__)

def all_products(request):
    # show all products view, Plus search and sort queries.

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:

        if 'sort' in request.GET:

            sortkey = request.GET['sort']

            sort = sortkey

            if sortkey == 'name':

                sortkey = 'lower_name'

                products = products.annotate(lower_name=Lower('name'))

            if sortkey == 'category':

                sortkey = 'category__name'

            if 'direction' in request.GET:

                direction = request.GET['direction']

                if direction == 'desc':

                    sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)

        if 'category' in request.GET:

            categories = request.GET['category'].split(',')

            products = products.filter(category__name__in=categories)

            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:

            query = request.GET['q']

            if not query:

                messages.error(request,

                               ("You didn't enter any search criteria!"))

                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)

            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {

        'products': products,

        'search_term': query,

        'current_categories': categories,

        'current_sorting': current_sorting,

    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Fetch all reviews related to the product with user information
    reviews = Review.objects.filter(product=product).select_related('user')
    
    # Define a range for ratings (1-5)
    ratings_range = list(range(1, 6))
    
    # Initialize review form
    form = ReviewForm()

    # Check if user is authenticated and retrieve their review if it exists
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()   

    # Prepare context for rendering
    context = {
        'product': product,
        'reviews': reviews,
        'ratings_range': ratings_range,
        'user_review': user_review,
        'form': form,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):

    # Allow superuser only to add
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you have tried a admin only request.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Success adding product to the store')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Form issues')
    else:
            form = ProductForm()

    template = 'products/add_product.html'
    context = {'form': form, }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):

    # Allow superuser only to add
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, store admin only request.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Form errors.')
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

    # Allow superuser only to add
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you have tried an admin-only request.')
        return redirect(reverse('home'))

    # If the user is a superuser, proceed with deleting the product
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product removed from store!')
    return redirect('products') 

@login_required
def add_review(request, product_id):
    """Allow users to add a review for a product."""
    product = get_object_or_404(Product, pk=product_id)

    if Review.objects.filter(user=request.user, product=product).exists():
        messages.error(request, 'You have already submitted a review for this product.')
        return redirect(reverse('product_detail', args=[product.id]))

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to submit your review. Please correct the errors below.')
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'product': product,
    }
    
    return render(request, 'products/add_review.html', context)


@login_required
def edit_review(request, product_id, review_id):
    
    product = get_object_or_404(Product, id=product_id)
    # Get the user's existing review for the product
    user_review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=user_review) 
        if form.is_valid():
            form.save() 
            return redirect('product_detail', product_id=product.id) 
    else:
        form = ReviewForm(instance=user_review)

    return render(request, 'products/edit_review.html', {'form': form, 'product': product, 'user_review': user_review})

@login_required
def delete_review(request, review_id):
    """Allow users to delete their own review."""
    review = get_object_or_404(Review, pk=review_id)

    if review.user != request.user:
        messages.error(request, "You do not have permission to delete this review.")
        return redirect('product_detail', product_id=review.product.id)

    review.delete()
    messages.success(request, 'Your review has been deleted successfully.')
    
    return redirect('product_detail', product_id=review.product.id)


@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'products/wishlist.html', {'wishlist': wishlist})

@login_required
def add_to_wishlist(request, product_id):
    print(f"Adding product with ID {product_id} to wishlist.")
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if product not in wishlist.products.all():
        wishlist.products.add(product)
        messages.success(request, f'{product.name} has been added to your wishlist!')
    else:
        messages.warning(request, f'{product.name} is already in your wishlist.')
    
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist')
