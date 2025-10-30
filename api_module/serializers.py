from rest_framework import serializers
from blog_module.models import Article
from shop_module.models import Product


class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['author', 'created_at', 'updated_at', 'status', 'rejected_reason', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['slug', 'created_at', 'updated_at']
