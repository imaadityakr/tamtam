from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

from . import models as qrcode_models
from django.contrib.auth import authenticate, get_user_model
User = get_user_model()

from datetime import datetime, timezone


class QRCodeSerializer(serializers.ModelSerializer):

    qr_id = serializers.CharField(source='qr_id.unique_code')

    default_error_messages = {
        'code-not-exist': 'Unique code does not exist.',
        'code-expired': 'Unique code has expired',
        }

    class Meta:
        fields = (
            'qr_id',
            'name',
            'email',
            'contact',
        )
        model = qrcode_models.QRCode

    def validate(self, data):

        try:
            qr_data =  data['qr_id']
            qr_id = qrcode_models.UniqueID.objects.get(unique_code=qr_data['unique_code'])
        except qrcode_models.UniqueID.DoesNotExist:
            raise serializers.ValidationError(
                self.error_messages['code-not-exist']
            )

        if qr_id:
            today = datetime.now(timezone.utc)
            if today > qr_id.expiry_date:
                raise serializers.ValidationError(
                    self.error_messages['code-expired']
                )

        return data

    def create(self, validated_data):
        qr_data = validated_data.pop('qr_id')
        unique_code = qr_data['unique_code']

        try:
            qr_id = qrcode_models.UniqueID.objects.get(unique_code=qr_data['unique_code'])
        except qrcode_models.UniqueID.DoesNotExist:
            raise serializers.ValidationError(
                self.error_messages['code-not-exist']
            )
        # qr = qrcode_models.QRCode.objects.create(qr_id=qr_id, **validated_data)
        # return qr
        qr, created = qrcode_models.QRCode.objects.update_or_create(qr_id=qr_id, defaults=validated_data)

        if created:
            return qr
        else:
            return qr

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