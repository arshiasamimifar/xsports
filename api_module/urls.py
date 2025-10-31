from django.urls import path
from .views import ArticleListApiView, ArticleDetailApiView, ArticleCreateApiView, ArticleDeleteApiView, ArticleUpdateApiView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', ArticleListApiView.as_view()),
    path('<int:pk>/', ArticleDetailApiView.as_view()),
    path('create/', ArticleCreateApiView.as_view()),
    path('delete/<int:pk>/', ArticleDeleteApiView.as_view()),
    path('update/<int:pk>/', ArticleUpdateApiView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]