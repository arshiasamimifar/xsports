from django.apps import AppConfig


class CartModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart_module'

    verbose_name = 'سبد خرید'
    verbose_name_plural = 'سبد خرید'
