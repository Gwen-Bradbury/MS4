from django.http import HttpResponse


class stripe_webhook_handler:
    """ Stripe Webhooks """
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Handle Webhook Events """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
            )
