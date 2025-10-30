from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from shop_module.models import Product
from .models import Cart, CartItem, Order
from .forms import CheckoutForm
from django.contrib import messages


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, "cart_module/cart_detail.html", {"cart": cart})


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart, created = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += 1
            item.save()
        return redirect("cart")


class DeleteFromCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, cart=cart, pk=pk)
        item.delete()
        return redirect('cart')


class UpdateQuantityView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, cart=cart, pk=pk)
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
        return redirect("cart")


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        checkout_form = CheckoutForm()
        context = {
            'checkout_form': checkout_form
        }
        return render(request, 'cart_module/checkout.html', context)

    def post(self, request):
        checkout_form = CheckoutForm(request.POST)
        cart = get_object_or_404(Cart, user=request.user)
        if checkout_form.is_valid():
            order = Order.objects.create(
                user=request.user,
                first_name=checkout_form.cleaned_data['first_name'],
                last_name=checkout_form.cleaned_data['last_name'],
                phone=checkout_form.cleaned_data['phone'],
                address=checkout_form.cleaned_data['address'],
                total_amount=cart.total_price_with_tax(),
            )
            order.status = 'paid'
            order.save()
            cart.items.all().delete()
            messages.success(
                request,
                '✅ به دلیل تستی بودن سایت، پرداخت واقعی انجام نشد اما سفارش شما با موفقیت ثبت و پرداخت شده در نظر گرفته شد.'
            )
            return redirect('cart')
        context = {
            'checkout_form': checkout_form
        }
        return render(request, 'cart_module/checkout.html', context)
