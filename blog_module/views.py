from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from account_module.models import CustomUser
from .forms import ArticleCommentForm
from .models import Article, ArticleCategory, ArticleComment


class ArticleListView(ListView):
    template_name = 'blog_module/article_list.html'
    queryset = Article.objects.published().order_by('-created_at')
    paginate_by = 3
    context_object_name = 'articles'


class ArticleDetail(DetailView):
    template_name = 'blog_module/article_detail.html'
    queryset = Article.objects.published()
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        context['comment'] = ArticleComment.objects.published().filter(article=article)
        context['comment_form'] = ArticleCommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'برای ارسال نظر باید اول وارد حساب کاربری شوید.')
            return redirect(request.path)
        self.object = self.get_object()
        comment_form = ArticleCommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, 'کامنت شما ثبت شد، طی 48 ساعت پس از تایید نمایش داده میشود.')
            return redirect(self.request.path_info)
        context = self.get_context_data()
        context['comment_form'] = comment_form
        return redirect(self.request.path_info)


def article_sidebar(request):
    latest_articles = Article.objects.published().order_by('-created_at')[:3]
    categories = ArticleCategory.objects.filter(is_active=True).annotate(count=Count('articles'))
    context = {
        'latest_articles': latest_articles,
        'categories': categories,
    }
    return render(request, 'blog_module/includes/sidebar.html', context)


class ArticleByCategory(ListView):
    template_name = 'blog_module/article_by_category.html'
    paginate_by = 3
    context_object_name = 'articles'

    def get_queryset(self):
        self.category = get_object_or_404(
            ArticleCategory, slug=self.kwargs['slug'], is_active=True
        )
        return self.category.articles.published().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ArticleByAuthor(ListView):
    template_name = 'blog_module/article_by_author.html'
    paginate_by = 3
    context_object_name = 'articles'

    def get_queryset(self):
        self.author = get_object_or_404(CustomUser, username=self.kwargs['username'])
        return (
            Article.objects.published()
            .filter(author=self.author)
            .select_related('author')
            .order_by('-created_at')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context


class ArticleSearchView(ListView):
    template_name = 'blog_module/article_list.html'
    context_object_name = 'articles'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q')
        qs = Article.objects.published()
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query) |
                Q(author__username__icontains=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context
