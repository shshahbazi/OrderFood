from django.urls import path

from .views import *

urlpatterns = [
    path('login/', AuthLoginUser.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('register/', UserRegistration.as_view()),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('forgot-pass-request/', ForgotPasswordRequest.as_view()),
    path('set-password/', SetPassword.as_view(), name='set-password'),
    path('get-user/<int:pk>/', GetUserProfile.as_view()),
    path('update-profile/<int:pk>/', UpdateProfile.as_view()),
    path('add-address/', AddAddress.as_view()),
    path('get-address/<int:pk>/', GetAddress.as_view()),
    path('get-user-address/', GetUserAddresses.as_view()),
    path('update-address/<int:pk>/', UpdateAddress.as_view()),
    path('add-fav-food/<int:pk>/', AddFavFood.as_view()),
    path('delete-fav-food/<int:pk>/', DeleteFavFood.as_view()),
    path('add-fav-res/<int:pk>/', AddFavRestaurant.as_view()),
]
