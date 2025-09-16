from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.utils import timezone


class User(AbstractUser):
    wallet = models.IntegerField(default=10000)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')
    amount_left = models.PositiveIntegerField()

    class Meta:
        ordering = ['-pk']


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.user.wallet -= self.product.price * self.quantity
        self.product.amount_left -= self.quantity
        with transaction.atomic():
            self.user.save()
            self.product.save()
            return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    @property
    def is_refundable(self):
        return (timezone.now() - self.created_at).total_seconds() < settings.ALLOWED_REFUND_TIME


class Refund(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='refund')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def delete(self, using = None, keep_parents = False, is_approved = False):
        if is_approved:
            self.order.product.amount_left += self.order.quantity
            self.order.user.wallet += self.order.product.price * self.order.quantity
            with transaction.atomic():
                self.order.product.save()
                self.order.user.save()
                return super().delete(using, keep_parents)
        else:
            return super().delete(using, keep_parents)

