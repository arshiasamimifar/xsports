from .serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from blog_module.models import Article
from rest_framework import status


class ArticleListApiView(APIView):
    def get(self, request):
        article = Article.objects.published()
        serializer = ArticleSerializer(article, many=True)
        return Response(serializer.data)


class ArticleDetailApiView(APIView):
    def get(self, request, pk):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


class ArticleCreateApiView(APIView):
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDeleteApiView(APIView):
    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response(status.HTTP_202_ACCEPTED)


class ArticleUpdateApiView(APIView):
    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)