from django.shortcuts import render


def index(request):
    """ Returns index.html """
    return render(request, 'home/index.html')
