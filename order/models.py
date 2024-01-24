from django.db import models
from customer.models import Profile, Card, Address
from django.core.validators import MaxValueValidator
from restaurant.models import Restaurant
from food.models import Food
from django.utils.crypto import get_random_string
import string


def create_order_number():
    while True:
        code = get_random_string(8, allowed_chars=string.ascii_uppercase + string.digits)
        if not Order.objects.filter(order_number=code).exists():
            return code


class Order(models.Model):
    STATUS_CHOICES = {
        ('UC', 'UpComing'),
        ('CN', 'Canceled'),
        ('CP', 'Complete'),
    }
    order_number = models.CharField(default=create_order_number, unique=False, editable=False, max_length=100)
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
    time_prepare_foods = models.IntegerField(default=0)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.food.name}  x{self.quantity} - {self.order.order_number} "


class PromoCode(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True)
    discount = models.IntegerField(blank=False)
    is_active = models.BooleanField(default=True)
