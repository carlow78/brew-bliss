from django.http import HttpResponse


class StripeWebook_Handler:
    # Stripe webhook handler

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        
        # Unexpected webhook event
        
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

