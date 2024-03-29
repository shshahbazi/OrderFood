from rest_framework import serializers

from .models import Order, OrderItem, PromoCode
from food.serializers import FoodSerializer
from customer.serializers import CardSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    credit_card = CardSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'
