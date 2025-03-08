from django.contrib import admin
from django.contrib import messages
from .models import Product, Transaction

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'total_price', 'date')

    def save_model(self, request, obj, form, change):
        if obj.product.stock >= obj.quantity:
            super().save_model(request, obj, form, change)
            messages.success(request, f"Transaksi berhasil: {obj.quantity} {obj.product.name} dibeli.")
        else:
            messages.warning(request, f"Stok tidak mencukupi untuk {obj.product.name}. Transaksi dibatalkan.")
