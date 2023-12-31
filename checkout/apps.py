from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    # This overrides the "ready" methos and imports the signals module
    def ready(self):
        import checkout.signals
