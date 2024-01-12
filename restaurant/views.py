from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from customer.models import Profile
from .models import Restaurant
from .serializers import RestaurantSerializer


class GetRestaurant(generics.RetrieveAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = (IsAuthenticated,)


class GetAllRestaurants(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'address', 'category', 'features__name']
    ordering_fields = ['rate', 'price_rating']
    ordering = ['-rate']
    permission_classes = (IsAuthenticated,)


class GetFavRestaurant(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        profile = get_object_or_404(Profile, id=self.request.user.id)
        return profile.fav_restaurant.all()


class FreeDeliveryRestaurant(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['-rate']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Restaurant.objects.filter(delivery_fee=0)


class DineInRestaurant(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['-rate']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Restaurant.objects.filter(dine_in=True)