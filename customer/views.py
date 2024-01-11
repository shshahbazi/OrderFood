from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
import jwt
from django.conf import settings
from smtplib import SMTPException

from food.models import Food
from restaurant.models import Restaurant
from .serializers import *


class AuthLoginUser(ObtainAuthToken):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_verified:
            return Response({'error': 'You are not verified!'}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            })


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            data={'message': f'Bye {request.user.full_name}!'},
            status=status.HTTP_204_NO_CONTENT
        )


def activation_link(request, user):
    token = RefreshToken.for_user(user).access_token

    current_site = get_current_site(request).domain
    relative_link = reverse('email-verify')

    absurl = 'http://' + current_site + relative_link + '?token=' + str(token)
    email_body = f'Hi {user.full_name}\nUse link below to verify your email\n{absurl}'
    email = EmailMessage(subject='Verify your email', body=email_body, to=[user.email])
    email.send()


class UserRegistration(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    serializer_class = ProfileRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_created = Profile.objects.get(email=serializer.data['email'])
            activation_link(request, user_created)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class VerifyEmail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = get_object_or_404(Profile, id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'message': 'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            activation_link(request, user)
            return Response({'error': 'Activation Expired, We will send you the activation email again.'},
                            status=status.HTTP_400_BAD_REQUEST)

        except jwt.DecodeError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            user = get_object_or_404(Profile, email=request.data['email'])
            activation_link(request, user)
            return Response({'message': 'Email Sent.'}, status=status.HTTP_200_OK)
        except SMTPException as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordRequest(APIView):
    permission_classes = (AllowAny,)

    def post(self, request,  *args, **kwargs):
        try:
            user = get_object_or_404(Profile, email=request.data['email'])
            token = RefreshToken.for_user(user).access_token

            current_site = get_current_site(request).domain
            relative_link = reverse('set-password')

            absurl = 'http://' + current_site + relative_link + '?token=' + str(token)
            email_body = f'Hi {user.full_name}\nUse link below to recovery your password\n{absurl}'
            email = EmailMessage(subject='Recovery your password', body=email_body, to=[user.email])
            email.send()
            return Response({'message': 'Email Sent.'}, status=status.HTTP_200_OK)
        except SMTPException as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


class SetPassword(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = Profile.objects.get(id=payload['user_id'])
            user.set_password(request.data['password'])
            user.save()
            return Response({'message': 'Password Set Successfully'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token Has Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class GetUserProfile(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)


class UpdateProfile(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()


class AddAddress(generics.CreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)


class GetAddress(generics.RetrieveAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes = (IsAuthenticated,)


class GetUserAddresses(generics.ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Address.objects.filter(user__id=self.request.user.id)


class UpdateAddress(generics.UpdateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes = (IsAuthenticated,)


class AddFavFood(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = get_object_or_404(Profile, id=request.user.id)
        food = get_object_or_404(Food, pk=pk)
        user.fav_foods.add(food)
        user.save()
        profile_serializer = ProfileSerializer(user)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)


class DeleteFavFood(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = get_object_or_404(Profile, id=request.user.id)
        food = get_object_or_404(Food, pk=pk)
        user.fav_foods.remove(food)
        user.save()
        profile_serializer = ProfileSerializer(user)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)


class AddFavRestaurant(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = get_object_or_404(Profile, id=request.user.id)
        restaurant = get_object_or_404(Restaurant, pk=pk)
        user.fav_restaurant.add(restaurant)
        user.save()
        profile_serializer = ProfileSerializer(user)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)


class DeleteFavRestaurant(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = get_object_or_404(Profile, id=request.user.id)
        restaurant = get_object_or_404(Restaurant, pk=pk)
        user.fav_restaurant.remove(restaurant)
        user.save()
        profile_serializer = ProfileSerializer(user)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)
