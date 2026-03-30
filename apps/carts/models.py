from django.db import models
from django.conf import settings
from apps.products.models import Product, Size

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def total_mrp(self):
        return sum(item.product.original_price * item.quantity for item in self.items.all())

    @property
    def total_amount(self):
        return sum(item.sub_total for item in self.items.all())

    @property
    def total_discount(self):
        return self.total_mrp - self.total_amount

    def __str__(self):
        return f"{self.user.username}'s cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def total_original_price(self):
        return self.product.original_price * self.quantity

    @property
    def sub_total(self):
        price = self.product.discount_price if self.product.discount_price else self.product.original_price
        return price * self.quantity

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')



