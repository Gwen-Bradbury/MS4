from decimal import Decimal
from django.conf import settings


def basket_items(request):

    basket_products = []
    total = 0
    item_count = 0
    delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)

    grand_total = delivery * total

    context = {
        'basket_products': basket_products,
        'total': total,
        'item_count': item_count,
        'delivery': delivery,
        'grand_total': grand_total
    }

    return context
