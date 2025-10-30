from .serializers import ArticleSerializer, ProductSerializer
from blog_module.permissions import IsAuthorOrSuperUserOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from blog_module.models import Article
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from shop_module.permissions import IsSuperUserOrReadOnly
from shop_module.models import Product


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class ArticleApiView(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrSuperUserOrReadOnly]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Article.objects.all()
        return Article.objects.filter(status='PB')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProductApiView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUserOrReadOnly]
