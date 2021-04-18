from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from gins.models import Gin


def basket_items(request):

    basket_products = []
    total = 0
    item_count = 0
    basket = request.session.get('basket', {})

    for item_id, quantity in basket.items():
        gin = get_object_or_404(Gin, pk=item_id)
        total += quantity * gin.price
        item_count += quantity
        basket_products.append({
            'item_id': item_id,
            'quantity': quantity,
            'gin': gin,
        })

    delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)

    grand_total = delivery + total

    context = {
        'basket_products': basket_products,
        'total': total,
        'item_count': item_count,
        'delivery': delivery,
        'grand_total': grand_total
    }

    return context
