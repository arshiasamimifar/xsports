from rest_framework.viewsets import ModelViewSet
from .serializers import ArticleSerializer
from blog_module.models import Article
from blog_module.permissions import IsInEditorsGroup
from rest_framework.permissions import IsAuthenticated


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.published()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsInEditorsGroup]