from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from .models import Restaurant
from .serializers import RestaurantSerializer


class GetRestaurant(generics.RetrieveAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = (IsAuthenticated,)


class GetAllRestaurants(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'address', 'category', 'features__name']
    permission_classes = (IsAuthenticated,)
