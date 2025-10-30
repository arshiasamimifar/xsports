from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.db.models import Count
from .forms import ProductCommentForm
from .models import Product, ProductCategory
from django.db.models import Q


class ProductListView(ListView):
    queryset = Product.objects.published()
    template_name = 'shop_module/product_list.html'
    paginate_by = 12
    context_object_name = 'products'


class ProductDetailView(DetailView):
    queryset = Product.objects.published()
    template_name = 'shop_module/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = ProductCommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'برای ارسال نظر باید اول وارد حساب کاربری شوید.')
            return redirect(request.path)
        self.object = self.get_object()

        product_comment_form = ProductCommentForm(request.POST)
        if product_comment_form.is_valid():
            comment = product_comment_form.save(commit=False)
            comment.product = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, 'کامنت شما ثبت شد، طی 48 ساعت پس از تایید نمایش داده میشود.')
        context = self.get_context_data()
        context['comment_form'] = product_comment_form
        return redirect(self.request.path_info)


def product_sidebar(request):
    category = ProductCategory.objects.published().annotate(count=Count('products'))
    latest_products = Product.objects.published().order_by('-created_at')[:3]
    context = {
        'category': category,
        'latest_products': latest_products,
    }
    return render(request, 'shop_module/includes/sidebar.html', context)


class ProductByCategory(ListView):
    template_name = 'shop_module/product_by_category.html'
    paginate_by = 3
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(ProductCategory, slug=self.kwargs['slug'], is_active=True)
        return self.category.products.published().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProductSearchView(ListView):
    template_name = 'shop_module/product_list.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q')
        qs = Product.objects.published()
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query) |
                Q(slug__icontains=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context
