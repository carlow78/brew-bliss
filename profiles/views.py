from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm

def profile(request):
   # Display user profile
    profile = get_object_or_404(UserProfile, user=request.user)
    orders = profile.orders.all()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully')

    form = UserProfileForm(instance=profile)
    template = 'profiles/profile.html'
    context = {
         'form': form,
         'orders': orders,
    }

    return render(request, template, context)