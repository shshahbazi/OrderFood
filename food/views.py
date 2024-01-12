from rest_framework import generics

from food.models import Food
from food.serializers import FoodSerializer


class GetFood(generics.RetrieveAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
