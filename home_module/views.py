from django.views.generic import ListView
from blog_module.models import Article


class HomeView(ListView):
    template_name = 'home_module/index.html'
    queryset = Article.objects.published().order_by('-created_at')[:6]
    context_object_name = 'articles'
