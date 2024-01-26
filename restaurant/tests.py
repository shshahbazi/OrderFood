from django.db import IntegrityError
from django.test import TestCase
from .models import Restaurant, RestaurantFeature
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator

class RestaurantModelTests(TestCase):
    def setUp(self):
        self.feature1 = RestaurantFeature.objects.create(name='Feature 1')
        self.feature2 = RestaurantFeature.objects.create(name='Feature 2')

    def test_create_restaurant(self):
        restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='Test Address',
            category='AS',
            rate=4.5,
            delivery_fee=2.99,
            arrival_time=45,
            open_time='12:00',
            dine_in=True,
            city='Test City',
            price_rating=3,
        )
        restaurant.features.add(self.feature1, self.feature2)

        self.assertEqual(restaurant.name, 'Test Restaurant')
        self.assertEqual(restaurant.address, 'Test Address')
        self.assertEqual(restaurant.category, 'AS')
        self.assertEqual(restaurant.rate, 4.5)
        self.assertEqual(restaurant.delivery_fee, 2.99)
        self.assertEqual(restaurant.arrival_time, 45)
        self.assertTrue(restaurant.dine_in)
        self.assertEqual(restaurant.city, 'Test City')
        self.assertEqual(restaurant.price_rating, 3)
        self.assertEqual(list(restaurant.features.all()), [self.feature1, self.feature2])

    def test_create_restaurant_invalid_rate(self):
        restaurant = Restaurant(
            name='Test Restaurant',
            category='AS',
            rate=6.0,  # Rate should be between 0 and 5
            delivery_fee=2.99,
            arrival_time=45,
            open_time='12:00',
            dine_in=True,
            city='Test City',
            price_rating=3,
            )
        self.assertRaises(ValidationError, restaurant.full_clean)

    def test_create_restaurant_missing_required_fields(self):
        with self.assertRaises(IntegrityError):
            Restaurant.objects.create(
                name='Test Restaurant',
                category='AS',
                rate=4.5,
                # Missing required fields: delivery_fee, arrival_time, open_time, dine_in, city
            )
