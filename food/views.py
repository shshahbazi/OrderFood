from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from food.models import Food
from food.serializers import FoodSerializer


class GetFood(generics.RetrieveAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    permission_classes = (IsAuthenticated,)


class GetAllFoods(generics.ListAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category', ]
    permission_classes = (IsAuthenticated,)


class GetRestaurantFood(generics.ListAPIView):
    serializer_class = FoodSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category', ]

    def get_queryset(self):
        try:
            return Food.objects.filter(restaurant__id=self.kwargs['pk'])
        except KeyError:
            return []
