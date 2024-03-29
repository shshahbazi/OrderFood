from django.urls import path

from .views import *

urlpatterns = [
    path('create-order/', CreateOrder.as_view()),
    path('get-order/<int:pk>/', GetOrder.as_view()),
    path('get-orders/', GetAllOrders.as_view()),
    path('apply-discount/', ApplyPromoCode.as_view()),
    path('update-order/<int:order_id>/', UpdateOrder.as_view()),
]