from rest_framework import serializers

from .models import Restaurant, RestaurantFeature


class RestaurantFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantFeature
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    features = RestaurantFeatureSerializer(read_only=True, many=True)

    class Meta:
        model = Restaurant
        fields = '__all__'
