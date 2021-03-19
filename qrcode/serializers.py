from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

from . import models as qrcode_models
from django.contrib.auth import authenticate, get_user_model
User = get_user_model()

class QRCodesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'email',
            'contact',
            'qrcode',
        )
        model = qrcode_models.QRCodes

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'}, )

    default_error_messages = {
    	'inactive_account': 'Your account is inactive. Please Confirm your account.',
        'not_superuser': 'Your account is not registered as super user.',
        'invalid_credentials': 'Sorry, we do not recognize that email or password. Please try again.',
    }

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'].lower())
        except User.DoesNotExist:
            raise serializers.ValidationError(
                self.error_messages['invalid_credentials']
            )

        if user and not user.is_active:
            raise serializers.ValidationError(
                self.error_messages['inactive_account']
            )

        if user and not user.is_superuser:
            raise serializers.ValidationError(
                self.error_messages['not_superuser']
            )
        self.user = authenticate(username=user.username, password=attrs.get('password'))

        if not self.user:
            raise serializers.ValidationError(
                self.error_messages['invalid_credentials'])
        return attrs

class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')
    is_superuser = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = (
            'auth_token', "is_superuser",
        )

    def get_is_superuser(self, obj):
        return obj.user.is_superuser