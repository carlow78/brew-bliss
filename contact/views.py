from django.shortcuts import render, redirect
from .forms import ContactUsForm
from .utils import send_notification

def contact(request):

    form = ContactUsForm(request.POST or None)

    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            contact = form.save()
            send_notification(contact)  # Send notification email
            return redirect('contactsuccess')  # Redirect to a success page
    
    return render(request, 'contact/contact.html', {'form': form})


def contact_success(request):
    return render(request, 'contact/success.html') 
