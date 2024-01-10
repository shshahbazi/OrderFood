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
    path('update-profile/<int:pk>/', UpdateProfile.as_view())
]
