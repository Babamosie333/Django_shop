from django.db import models
from django.contrib.auth.models import User
from products.models import Product


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, blank=True, null=True) # Stripe Session ID
    payment_method = models.CharField(max_length=50, blank=True, null=True) # e.g., 'Stripe'
    models.BooleanField(default=False)
    status = models.CharField(max_length=20, default="processing", choices=[("processing", "Processing"), ("shipped", "Shipped"), ("delivered", "Delivered"), ("cancelled", "Cancelled")])

    def _str_(self):
        return f"Order #{self.pk} for {self.user.username}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.price * self.quantity