from django.shortcuts import (
    render,
    redirect,
    reverse,
    HttpResponse,
    get_object_or_404
)
from django.contrib import messages
from gins.models import Gin


def view_basket(request):
    """ Returns basket.html """
    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id):
    """ Add an Amount of Specified Gin to Basket """
    gin = get_object_or_404(Gin, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    basket = request.session.get('basket', {})

    if item_id in list(basket.keys()):
        basket[item_id] += quantity
        messages.success(request,
                         f'Updated { gin.name } amount to {basket[item_id]}')
    else:
        basket[item_id] = quantity
        messages.success(request, f'Added { gin.name } to your basket')

    request.session['basket'] = basket
    return redirect(redirect_url)


def adjust_basket(request, item_id):
    """ Adjust the Amount of Specified Gin in the Basket """
    gin = get_object_or_404(Gin, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    basket = request.session.get('basket', {})

    if quantity > 0:
        basket[item_id] = quantity
        messages.success(request,
                         f'Updated { gin.name } amount to {basket[item_id]}')
    else:
        """ Remove Gin From Basket """
        basket.pop(item_id)
        messages.success(request, f'{ gin.name } removed from your basket')

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))


def remove_from_basket(request, item_id):
    """ Remove Gin From Basket """
    try:
        gin = get_object_or_404(Gin, pk=item_id)
        basket = request.session.get('basket', {})

        basket.pop(item_id)
        messages.success(request, f'{ gin.name } removed from your basket')

        request.session['basket'] = basket
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
