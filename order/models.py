from django.db import models
from customer.models import Profile, Card, Address
from django.core.validators import MaxValueValidator
from restaurant.models import Restaurant
from food.models import Food
import uuid


class Order(models.Model):
    STATUS_CHOICES = {
        ('UC', 'UpComing'),
        ('CN', 'Canceled'),
        ('CP', 'Complete'),
    }
    order_number = models.CharField(default=str(uuid.uuid4().hex), unique=True, editable=False, max_length=100)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    review = models.DecimalField(default=0, decimal_places=1, max_digits=3,
                                 validators=[MaxValueValidator(5.0)])
    total_price = models.DecimalField(blank=False, decimal_places=2, max_digits=4, default=0)
    credit_card = models.ForeignKey(Card, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    registration_time = models.DateTimeField(auto_now=True)
    delivery_time = models.DateTimeField()
    status = models.CharField(max_length=500, choices=STATUS_CHOICES, default='UC')

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.food.name}  x{self.quantity} "


class PromoCode(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True)
    discount = models.IntegerField(blank=False)
    is_active = models.BooleanField(default=True)
