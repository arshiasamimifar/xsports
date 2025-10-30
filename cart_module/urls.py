from django.urls import path
from .views import AddToCartView, CartView, DeleteFromCartView, UpdateQuantityView, CheckoutView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete-form-cart/<int:pk>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('update-quantity/<int:pk>/', UpdateQuantityView.as_view(), name='update_quantity'),
]
