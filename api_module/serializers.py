from rest_framework import serializers
from blog_module.models import Article, ArticleCategory


class ArticleSerializer(serializers.Serializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=ArticleCategory.objects.published(),
        many=True
    )
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    body = serializers.CharField(max_length=2500)
    image = serializers.ImageField()
    author = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(max_length=20, read_only=True)
    slug = serializers.SlugField(read_only=True)

    def create(self, validated_data):
        categories = validated_data.pop('category', [])
        article = Article.objects.create(**validated_data)
        article.category.set(categories)
        return article

    def update(self, instance, validated_data):
        categories = validated_data.pop('category', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if categories is not None:
            instance.category.set(categories)
        return instance
