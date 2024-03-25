from django.db import models

# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.PositiveIntegerField(help_text='Discount in percentage')
    active = models.BooleanField(default = True)
    active_date = models.DateField()
    expiry_date = models.DateField()
    required_amount = models.PositiveBigIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.code