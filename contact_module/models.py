from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models


class Contact(models.Model):
    full_name = models.CharField(
        max_length=72,
        validators=[
            MinLengthValidator(6),
            MaxLengthValidator(72),
        ],
        verbose_name='نام و نام خانوادگی',
    )

    phone = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(regex=r'^09\d{9}$', message="شماره تلفن باید با 09 شروع شود و شامل ۱۱ رقم باشد."),
        ],
        verbose_name='تلفن همراه',
    )

    message = models.TextField(verbose_name='پیام')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_readed = models.BooleanField(default=False, verbose_name='خوانده شده خوانده نشده')

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def __str__(self):
        return self.full_name