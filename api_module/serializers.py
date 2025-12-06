from rest_framework import serializers
from blog_module.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['id', 'status', 'slug', 'author', 'created_at', 'updated_at', 'rejected_reason']