from django.shortcuts import render


def view_basket(request):
    """ Returns basket.html """
    return render(request, 'basket/basket.html')
