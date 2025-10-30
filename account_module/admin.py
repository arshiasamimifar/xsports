from django.contrib import admin
from .models import CustomUser
from django.utils.html import format_html


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'image_tag', 'phone_number', 'is_active', 'is_author']
    list_filter = ['is_active', 'is_author']
    search_fields = ['email', 'phone_number']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" />', obj.image.url)
        return "-"

    image_tag.short_description = 'تصویر'
