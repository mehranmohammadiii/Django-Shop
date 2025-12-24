from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'

    def ready(self):
        """
        This method is called when the app is ready.
        It can be used to import signals or perform any startup tasks.
        """
        # Importing signals to ensure they are registered
        import cart.signals  # noqa: F401
        return super().ready()
