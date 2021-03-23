from . import models as qrcode_models
from . import serializers as qrcode_serializer

from django.conf import settings
from django.contrib.auth import user_logged_in, user_logged_out, get_user_model

from rest_framework import (
    generics, permissions, response, status, views, exceptions)

from rest_framework.permissions import IsAdminUser

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

class ListProduct(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        )
    queryset = qrcode_models.QRCode.objects.all()
    serializer_class = qrcode_serializer.QRCodeSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = qrcode_serializer.LoginSerializer
    permission_classes = (
        permissions.AllowAny,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            user_logged_in.send(
                sender=user.__class__, request=self.request, user=user)
            return response.Response(
                data=qrcode_serializer.TokenSerializer(token).data,
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

class LogoutView(views.APIView):
    permission_classes = (
        permissions.IsAuthenticated,
        )

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        user_logged_out.send(
            sender=request.user.__class__,
            request=request,
            user=request.user)
        return response.Response(status=status.HTTP_200_OK)