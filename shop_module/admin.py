from django.contrib import admin
from .models import Color, Product, ProductKeyFeature, ProductCategory, ProductAdditionalInformation, ProductComment


class ProductKeyFeaturesInline(admin.TabularInline):
    model = ProductKeyFeature
    extra = 0
    min_num = 0
    can_delete = True


class ProductAdditionalInformationInline(admin.TabularInline):
    model = ProductAdditionalInformation
    extra = 0
    min_num = 0
    can_delete = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductKeyFeaturesInline, ProductAdditionalInformationInline]
    list_display = ['title', 'image_tag', 'slug', 'price', 'created_at', 'updated_at', 'is_active', 'stock']
    list_filter = ['created_at', 'is_active', 'stock']
    search_fields = ['title', 'body', 'slug', 'price']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    search_fields = ['title', ]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active']
    list_filter = ['is_active', ]
    search_fields = ['title', 'slug']


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'author', 'is_active', 'created_at']