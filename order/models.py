from django.db import models
from django.conf import settings
from product.models import Product
from cart.models import Coupon


# Create your models here.
class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, related_name='ordered', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return f"{self.product.title} x {self.quantity}"

    @property
    def total(self):
        return float(self.price) * float(self.quantity)

class Order(models.Model):
    STATUS = ('Recieved', 'On the way', 'Delivered')
    PAYMENT_METHOD = ('PayPal', 'SSLcommerz')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='orders', on_delete=models.CASCADE)
    order_items = models.ManyToManyField(OrderItem)
    coupon = models.ForeignKey(
        Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    address = models.TextField()
    total = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=True)
    payment_method = models.CharField(max_length=150, choices=list(
        zip(PAYMENT_METHOD, PAYMENT_METHOD)), default='PayPal')
    transaction_id = models.UUIDField()
    paypal_transaction_id = models.CharField(
        max_length=50, null=True, blank=True)
    status = models.CharField(max_length=15, choices=list(
        zip(STATUS, STATUS)), default='Recieved')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name
