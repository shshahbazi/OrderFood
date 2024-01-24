from django.db.models import Max
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import OrderItem, Order
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