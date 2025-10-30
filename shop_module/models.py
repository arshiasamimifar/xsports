from django.db import models
from django.utils.html import format_html

from account_module.models import CustomUser
from .managers import ProductManager, ProductCategoryManager, ProductCommentsManager


class Color(models.Model):
    title = models.CharField(max_length=20, verbose_name='عنوان')

    class Meta:
        verbose_name = 'رنگ بندی'
        verbose_name_plural = 'رنگ بندی ها'

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    title = models.CharField(max_length=20, verbose_name='عنوان')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    slug = models.SlugField(unique=True, verbose_name='آدرس')
    objects = ProductCategoryManager()

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='نام محصول')
    body = models.TextField(verbose_name='توضیحات محصولات')
    slug = models.SlugField(max_length=50, unique=True, blank=True, editable=False, verbose_name='آدرس')
    price = models.IntegerField(verbose_name='قیمت')
    image = models.ImageField(upload_to='products', verbose_name='تصویر')
    color = models.ManyToManyField(Color, related_name='products', verbose_name='رنگ')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products', verbose_name='دسته بندی')
    discount = models.PositiveSmallIntegerField(default=0, verbose_name='تخفیف')
    stock = models.PositiveIntegerField(default=0, verbose_name='موجودی')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ آپدیت')
    objects = ProductManager()

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = self.title.replace(' ', '+')
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" width="100" />', self.image.url)
        return "—"

    image_tag.short_description = "تصویر"


class ProductKeyFeature(models.Model):
    title = models.CharField(max_length=60, verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='key_features', verbose_name='محصول')

    class Meta:
        verbose_name = 'ویژگی های محصول'
        verbose_name_plural = 'ویژگی های محصولات'

    def __str__(self):
        return self.title


class ProductAdditionalInformation(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ProductAdditionalInformations', verbose_name='اطلاعات اضافی')

    class Meta:
        verbose_name = 'اطلاعات اضافی'
        verbose_name_plural = 'اطلاعات اضافی'

    def __str__(self):
        return self.title


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصول')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_product_comment', verbose_name='نویسنده')
    body = models.TextField(verbose_name='متن نظر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    objects = ProductCommentsManager()

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'