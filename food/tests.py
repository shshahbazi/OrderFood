from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from customer.models import Profile
from .models import Food
from restaurant.models import Restaurant
from django.core.exceptions import ValidationError

from .serializers import FoodSerializer


class FoodModelTests(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='Test Address',
            category='AS',
            rate=4.5,
            delivery_fee=2.99,
            arrival_time=45,
            open_time='12:00:00',
            dine_in=True,
            city='Test City',
            price_rating=3,
        )

    def test_create_food(self):
        food = Food.objects.create(
            name='Test Food',
            restaurant=self.restaurant,
            category='AS',
            rate=4.5,
            prepare_time=30,
            price=12.99,
            picture='path/to/picture.jpg',
        )
        self.assertEqual(food.name, 'Test Food')
        self.assertEqual(food.restaurant, self.restaurant)
        self.assertEqual(food.category, 'AS')
        self.assertEqual(food.rate, 4.5)
        self.assertEqual(food.prepare_time, 30)
        self.assertEqual(food.price, 12.99)
        self.assertEqual(food.picture, 'path/to/picture.jpg')

    def test_create_food_invalid_rate(self):
        food = Food(name='Test Food',
                    restaurant=self.restaurant,
                    category='AS',
                    rate=6.0,  # Rate should be between 0 and 5
                    prepare_time=30,
                    price=12.99,
                    picture='path/to/picture.jpg',
                )
        self.assertRaises(ValidationError, food.full_clean)


class FoodViewsTests(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='Test Address',
            category='AS',
            rate=4.5,
            delivery_fee=2.99,
            arrival_time=45,
            open_time='12:00:00',
            dine_in=True,
            city='Test City',
            price_rating=3,
        )
        self.user = Profile.objects.create_user(
            email='test@example.com',
            password='testpassword',
            full_name='John Doe',
            is_verified=True
        )
        self.food = Food.objects.create(
            name='Test Food',
            restaurant=self.restaurant,
            category='AS',
            rate=4.5,
            prepare_time=30,
            price=12.99,
        )
        self.client = APIClient()
        response = self.client.post('/login/', data={'email': 'test@example.com', 'password': 'testpassword'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    def test_get_food(self):
        response = self.client.get(f'/get-food/{self.food.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, FoodSerializer(self.food).data)

