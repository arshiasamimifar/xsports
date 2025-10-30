# cart_module/models.py
from django.db import models
from django.conf import settings
from shop_module.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name='کاربر'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'سبد خرید کاربر'
        verbose_name_plural = 'سبد خرید کاربر'

    def total_price(self):
        """جمع کل قیمت همه آیتم‌های سبد"""
        return sum(item.total_price() for item in self.items.all())

    def total_price_with_tax(self):
        """جمع کل با مالیات 10 درصد"""
        tax_rate = 0.10
        return int(self.total_price() * (1 + tax_rate))

    def tax_price(self):
        """مقدار مالیات 10 درصد"""
        tax_rate = 0.12
        return int(self.total_price() * tax_rate)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name='سبد خرید کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')

    class Meta:
        unique_together = ('cart', 'product')
        verbose_name = 'محصولات سبد خرید'
        verbose_name_plural = 'محصولات سبد خرید'

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('failed', 'ناموفق'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن')
    address = models.TextField(verbose_name='آدرس')
    total_amount = models.PositiveIntegerField(verbose_name='قیمت کل')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return f"سفارش {self.id} - {self.user}"
