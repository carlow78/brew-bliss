from django.shortcuts import render

def index(request):

    # index (home) view
    
    return render(request, 'home/index.html')


def newsletter(request):

    return render(request, 'home/newsletter.html')
