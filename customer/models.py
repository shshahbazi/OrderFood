from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .validators import PhoneValidator
from restaurant.models import Restaurant
from food.models import Food


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Profile(AbstractUser):
    username = None
    full_name = models.CharField(max_length=500, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False)
    picture = models.FileField()
    phone = models.CharField(max_length=50, validators=[PhoneValidator], blank=True)
    fav_restaurant = models.ManyToManyField(Restaurant)
    fav_foods = models.ManyToManyField(Food)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.full_name


class Address(models.Model):
    CATEGORY_CHOICES = {
        ('H', 'Home'),
        ('W', 'Work'),
    }
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    street = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    zip_code = models.CharField(max_length=500)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='H')


class Card(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=100)

    def __str__(self):
        return self.card_number
