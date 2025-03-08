from django.db import models
from django.db.models import F
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Validasi sebelum menyimpan transaksi"""
        if not self.product:
            raise ValidationError("Produk tidak boleh kosong")

        if self.quantity <= 0:
            raise ValidationError("Kuantitas harus lebih dari 0")

        product_stock = Product.objects.filter(id=self.product.id).values_list('stock', flat=True).first()

        if product_stock is None:
            raise ValidationError("Produk tidak ditemukan")

        if product_stock < self.quantity:
            raise ValidationError("Stok tidak mencukupi untuk transaksi ini.")

    def save(self, *args, **kwargs):
        """Kurangi stok hanya jika validasi lolos"""
        self.clean()  # Panggil validasi sebelum menyimpan

        # Hitung total harga transaksi
        self.total_price = self.product.price * self.quantity

        # Kurangi stok produk
        Product.objects.filter(id=self.product.id).update(stock=F('stock') - self.quantity)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"
