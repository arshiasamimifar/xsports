from django.contrib import admin
from django.utils.html import format_html

from .models import Article, ArticleCategory, ArticleComment


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active']
    list_filter = ['is_active', ]
    search_fields = ['title', ]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image_tag', 'author', 'created_at', 'updated_at', 'slug', 'status']
    list_filter = ['created_at', 'updated_at', 'status']
    search_fields = ['title', 'body', 'author__username', 'author__first_name', 'author__last_name']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"

    image_tag.short_description = 'تصویر'


@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'author', 'create_at', 'is_active']
    list_filter = ['article', 'create_at', 'is_active', 'author__username']
    search_fields = ['article__title', 'author__username', 'author__first_name', 'author__last_name']
