from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWebhookHandler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """ Listen for Stripe Webhooks """
    """ Setup """
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    stripe.api_key = settings.STRIPE_CLIENT_SECRET
    """ Get Webhook Data and Verify Signature """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        """ Invalid Payload """
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        """ Invalid Signature """
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(content=e, status=400)

    """ Set Up Webhook Handler """
    handler = StripeWebhookHandler(request)

    """ Map Webhooks To Relevant Handler Functions """
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_failed,
    }

    """ Get Webhook Type From Stripe """
    event_type = event['type']

    """ If it Has Handler, Get It From Event Map """
    """ Use Generic One By Default """
    event_handler = event_map.get(event_type, handler.handle_event)

    """ Call Event Handler with Event """
    response = event_handler(event)
    return response
