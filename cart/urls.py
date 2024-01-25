from django.urls import path

from .views import *

urlpatterns = [
    path('cart/', CartDetail.as_view()),
    path('cart/add/<int:food_id>/', AddToCart.as_view()),
    path('cart/remove/<int:food_id>/', RemoveFromCart.as_view()),
    path('cart/get-restaurant/', GetCartRestaurant.as_view())
]