from django.urls import path

from .views import *

urlpatterns = [
    path('get-restaurant/<int:pk>/', GetRestaurant.as_view()),
]
