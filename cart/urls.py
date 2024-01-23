from django.urls import path

from .views import *

urlpatterns = [
    path('cart/add/<int:food_id>/', AddToCart.as_view()),
]