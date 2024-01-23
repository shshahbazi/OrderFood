from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.forms.models import model_to_dict
from food.models import Food
from .cart import Cart


class AddToCart(APIView):
    def get(self, request, food_id):
        # create a new cart object passing it the request object
        cart = Cart(request)
        food = get_object_or_404(Food, id=food_id)
        cart.add(food)
        return Response(status=status.HTTP_200_OK)


class CartDetail(APIView):
    def get(self, request):
        data = []
        cart = Cart(request)
        for item in cart:
            item['food'] = model_to_dict(item['food'])
            data.append(item)
        return Response(data)