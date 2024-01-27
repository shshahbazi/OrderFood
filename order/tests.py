from django.test import TestCase

from food.models import Food
from .models import Order, OrderItem
from customer.models import Profile, Card, Address
from restaurant.models import Restaurant
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.test import APIClient


class OrderModelTests(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(email='test@example.com', password='testpassword', full_name='John Doe',
                                              is_verified=True)
        self.restaurant = Restaurant.objects.create(name='Test Restaurant', category='AS', rate=4.5, delivery_fee=2.99,
                                                    arrival_time=45, open_time='12:00', dine_in=True, city='Test City',
                                                    price_rating=3)
        self.card = Card.objects.create(card_number='1234567890123456', user=self.profile)
        self.address = Address.objects.create(city='Test City', street='Test Street', zip_code='12345', state='Test',
                                              user=self.profile)

    def test_create_order(self):
        order = Order.objects.create(
            user=self.profile,
            total_price=30.99,
            credit_card=self.card,
            restaurant=self.restaurant,
            delivery_address=self.address,
            delivery_time=timezone.now(),
            status='UC',
            time_prepare_foods=45,
        )
        self.assertEqual(order.user, self.profile)
        self.assertEqual(order.status, 'UC')

class OrderViewsTests(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create_user(
            email='test@example.com',
            password='testpassword',
            full_name='John Doe',
            is_verified=True
        )
        self.restaurant = Restaurant.objects.create(name='Test Restaurant', category='AS', rate=4.5, delivery_fee=2.99,
                                                    arrival_time=45, open_time='12:00', dine_in=True, city='Test City',
                                                    price_rating=3)
        self.card = Card.objects.create(card_number='1234567890123456', user=self.profile)
        self.address = Address.objects.create(city='Test City', street='Test Street', zip_code='12345', state='Test',
                                              user=self.profile)
        self.food = Food.objects.create(name='Test Food', restaurant=self.restaurant, category='AS', rate=4.5,
                                        prepare_time=30, price=12.99)

        self.client = APIClient()
        response = self.client.post('/login/', data={'email': 'test@example.com', 'password': 'testpassword'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])


    def test_get_order(self):
        order = Order.objects.create(
            user=self.profile,
            total_price=30.99,
            credit_card=self.card,
            restaurant=self.restaurant,
            delivery_address=self.address,
            delivery_time='2024-01-25T12:00:00Z',
            status='UC',
        )
        OrderItem.objects.create(order=order, food=self.food, quantity=2)

        response = self.client.get(f'/get-order/{order.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total_price'], '30.99')
        self.assertEqual(response.data['status'], 'UC')
        self.assertEqual(len(response.data['order_items']), 1)
