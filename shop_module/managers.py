from django.db import models


class ProductManager(models.Manager):
    def published(self):
        return self.filter(is_active=True)


class ProductCategoryManager(models.Manager):
    def published(self):
        return self.filter(is_active=True)


class ProductCommentsManager(models.Manager):
    def published(self):
        return self.filter(is_active=True)
