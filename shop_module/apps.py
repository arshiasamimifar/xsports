from django.apps import AppConfig


class ShopModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop_module'

    verbose_name = 'فروشگاه'
    verbose_name_plural = 'فروشگاه'
