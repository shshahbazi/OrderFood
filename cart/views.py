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
            item['food'] = model_to_dict(item['food'], fields=['id', 'name'])
            data.append(item)
        return Response({
            'items': data,
            'total_cart_price': cart.get_total_price(),
            'discount_price': cart.get_discount(),
            'total_price_after_discount': cart.get_total_price_after_discount()
            })


class RemoveFromCart(APIView):
    def get(self, request, food_id):
        cart = Cart(request)
        food = get_object_or_404(Food, id=food_id)
        cart.remove(food)
        return Response(status=status.HTTP_200_OK)


class GetCartRestaurant(APIView):
    def get(self, request):
        cart = Cart(request)
        try:
            for item in cart:
                item['food'] = model_to_dict(item['food'], fields=['id', 'name'])
            print(next(iter(cart.cart.values())))
            restaurant_id = Food.objects.get(id=next(iter(cart.cart.values()))['food']['id']).restaurant.id
            return Response({'id': restaurant_id}, status=status.HTTP_200_OK)
        except :
             return Response({'id': 'empty cart'}, status=status.HTTP_400_BAD_REQUEST)
