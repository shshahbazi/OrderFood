from django.db import models
from django.core.validators import MaxValueValidator


class RestaurantFeature(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    CATEGORY_CHOICES ={
        ('AS', 'Asian'),
        ('IT', 'Italian'),
        ('CH', 'Chicken'),
        ('FI', 'Fish'),
        ('BU', 'Burger'),
        ('PI', 'Pizza'),
        ('DS', 'Dessert')
    }

    name = models.CharField(max_length=500)
    background_pic = models.FileField()
    icon = models.FileField()
    description = models.TextField()
    address = models.CharField(max_length=500)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    rate = models.DecimalField(default=0, decimal_places=1, max_digits=3,
                               validators=[MaxValueValidator(5.0)])
    delivery_fee = models.DecimalField(blank=False, decimal_places=2, max_digits=4, default=0)
    arrival_time = models.IntegerField(default=0)
    features = models.ManyToManyField(RestaurantFeature)
    open_time = models.TimeField()
    dine_in = models.BooleanField(default=False)
    city = models.CharField(max_length=100)
    price_rating = models.IntegerField(default=1)

    def __str__(self):
        return self.name
