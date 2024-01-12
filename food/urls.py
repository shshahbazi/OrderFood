from django.urls import path

from .views import *

urlpatterns = [
    path('get-food/<int:pk>/', GetFood.as_view()),
    path('get-foods/', GetAllFoods.as_view()),
]