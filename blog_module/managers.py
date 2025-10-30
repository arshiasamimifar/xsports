from django.db import models


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='PB')


class ArticleCategoryManager(models.Manager):
    def published(self):
        return self.filter(is_active=True)


class ArticleCommentManager(models.Manager):
    def published(self):
        return self.filter(is_active=True)