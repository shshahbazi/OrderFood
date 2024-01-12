from django.urls import path

from .views import *

urlpatterns = [
    path('get-restaurant/<int:pk>/', GetRestaurant.as_view()),
    path('get-restaurants/', GetAllRestaurants.as_view()),
    path('get-fav-restaurants/', GetFavRestaurant.as_view())
]
