from django.test import TestCase
from .models import Article


class ArticleModelTest(TestCase):
    def test_str_method(self):
        article = Article.objects.create(title="Test Title")
        self.assertEqual(str(article), "Test Title")
