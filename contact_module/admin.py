from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'create_at', 'message', 'is_readed']
    list_filter = ['create_at', 'is_readed']
    search_fields = ['full_name', 'phone', 'create_at', 'message']