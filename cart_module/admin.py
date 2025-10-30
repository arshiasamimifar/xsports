from django.contrib import admin
from .models import Cart, CartItem, Order


# ====== CartItem Inline ======
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'total_price')
    can_delete = False

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = "قیمت کل آیتم"


# ====== Cart Admin ======
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'total_cart_price']
    inlines = [CartItemInline]

    def total_cart_price(self, obj):
        return obj.total_price_with_tax()
    total_cart_price.short_description = 'جمع کل با مالیات'


# ====== OrderItem Inline (اگر بخوای آیتم‌ها رو هم نگه داری) ======
# فعلا چون OrderItem نداریم، فقط Order خودشه
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'phone', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'first_name', 'last_name', 'phone', 'address']
    ordering = ['-created_at']
    readonly_fields = ['total_amount', 'created_at']
