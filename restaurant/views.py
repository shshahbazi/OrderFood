from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Restaurant
from .serializers import RestaurantSerializer


class GetRestaurant(generics.RetrieveAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = (IsAuthenticated,)
