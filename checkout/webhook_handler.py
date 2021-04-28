from django.http import HttpResponse


class StripeWebhookHandler:
    """ Stripe Webhooks """
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Handle Unknown/Unexpected Webhooks """
        return HttpResponse(
            content=f'Unhandled Webhook received: {event["type"]}',
            status=200
            )

    def handle_payment_succeeded(self, event):
        """ Handle payment_intent.succeeded Webhook """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
            )

    def handle_payment_failed(self, event):
        """ Handle payment_intent.payment_failed Webhook """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
            )
