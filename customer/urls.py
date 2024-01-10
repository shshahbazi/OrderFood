from django.urls import path

from .views import *

urlpatterns = [
    path('login/', AuthLoginUser.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]