from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OrderItem, Order, PromoCode
from .serializers import OrderSerializer
from cart.cart import Cart


class CreateOrder(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        cart = Cart(request)
        if serializer.is_valid():
            order = serializer.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    food=item['food'],
                    quantity=item['quantity']
                )
            max_prepare_time = order.orderitem_set.all().aggregate(max_time=Max('food__prepare_time', default=0))
            order.time_prepare_foods = max_prepare_time['max_time']
            cart.clear()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class GetOrder(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)


class GetAllOrders(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user__id=self.request.user.id)


class ApplyPromoCode(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        coupon = get_object_or_404(PromoCode, code=request.data['code'])
        if coupon.user.id == request.user.id:
            if coupon.is_active:
                request.session['coupon_id'] = coupon.id
                coupon.is_active = False
                coupon.save()
                return Response({'discount': 'Promo code applied successfully'}, status=status.HTTP_200_OK)
            return Response({'discount': 'This code is not active.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'discount': 'This code does not belong to you.'}, status=status.HTTP_400_BAD_REQUEST)




class UpdateOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order_serializer = OrderSerializer(
            instance=order,
            data=request.data,
            partial=True
        )
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data, status=status.HTTP_200_OK)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
