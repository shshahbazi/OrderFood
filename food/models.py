from django.db import models
from django.core.validators import MaxValueValidator
from restaurant.models import Restaurant


class Food(models.Model):
    CATEGORY_CHOICES = {
        ('AS', 'Asian'),
        ('IT', 'Italian'),
        ('CH', 'Chicken'),
        ('FI', 'Fish'),
        ('BU', 'Burger'),
        ('PI', 'Pizza'),
        ('DS', 'Dessert')
    }

    name = models.CharField(max_length=600)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='AS')
    rate = models.DecimalField(default=0, decimal_places=1, max_digits=3,
                               validators=[MaxValueValidator(5.0)])
    prepare_time = models.IntegerField(default=0)
    price = models.DecimalField(blank=False, decimal_places=2, max_digits=4, default=0)

    def __str__(self):
        return f"{self.name}  {self.restaurant.name}"
