from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from food.models import Food
from .cart import Cart


class AddToCart(APIView):
    def get(self, request, food_id):
        # create a new cart object passing it the request object
        cart = Cart(request)
        food = get_object_or_404(Food, id=food_id)
        cart.add(food)
        return Response(status=status.HTTP_200_OK)
