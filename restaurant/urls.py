from django.urls import path

from .views import *

urlpatterns = [
    path('get-restaurant/<int:pk>/', GetRestaurant.as_view()),
    path('get-restaurants/', GetAllRestaurants.as_view()),
    path('get-fav-restaurants/', GetFavRestaurant.as_view()),
    path('restaurants/free-delivery/', FreeDeliveryRestaurant.as_view()),
    path('restaurants/dine-in/', DineInRestaurant.as_view()),
    path('restaurants/nearest/<str:city>', NearestRestaurant.as_view()),
    path('restaurants/popular/', PopularRestaurant.as_view()),
]
