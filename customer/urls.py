from django.urls import path

from .views import *

urlpatterns = [
    path('login/', AuthLoginUser.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('register/', UserRegistration.as_view()),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
]