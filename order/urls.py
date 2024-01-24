from django.urls import path

from .views import *

urlpatterns = [
    path('create-order/', CreateOrder.as_view()),
    path('get-order/<int:pk>/', GetOrder.as_view()),
]