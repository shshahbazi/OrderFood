from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .serializers import *


class AuthLoginUser(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_verified:
            return Response({'error': 'You are not verified!'}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
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