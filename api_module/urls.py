from rest_framework.routers import DefaultRouter
from .views import ArticleApiView, ProductApiView

router = DefaultRouter()
router.register(r'article', ArticleApiView, basename='article_api')
router.register(r'product', ProductApiView, basename='product_api')
urlpatterns = router.urls
