from rest_framework import serializers
from .models import User
from rentit import settings
from rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer
from . import google
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed
from datetime import date, timedelta

class RegisterUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    birth_date = serializers.DateField(required=True)
    message = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "birth_date",
            "email",
            "phone",
            "password",
            "front_pictures",
            "back_pictures",
            "face_pictures",
            "address",
            'message',
        )

    def get_message(self, obj):
        return (
            "Verification message has been sent to your email, please verify your email"
        )

    def validate_phone(self, value):
        if not value[1:].isnumeric():
            raise serializers.ValidationError('Phone must be numeric symbols')
        if value[:4] != '+996':
            raise serializers.ValidationError('Phone number should start with +996 ')
        elif len(value) != 13:
            raise serializers.ValidationError("Phone number must be 13 characters long")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "role"]


class PasswordResetSerializer(_PasswordResetSerializer):

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'EMAIL_HOST_USER'),

            'email_template_name': 'reset_password.html',

            'request': request
        }
        self.reset_form.save(**opts)

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError('Error')

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Invalid e-mail address')

        return value


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(provider=provider, user_id=user_id, email=email, name=name)


class UserListSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'birth_date',
            'age',
            'is_active',
            'front_pictures',
            'back_pictures',
            'face_pictures',
            'email',
            'phone',
            'address',
            'role',
            'is_staff',
            'is_active',
            'is_superuser',
            'date_joined',
              ]
        read_only_fields = ['is_active']

    def get_age(self, obj):
        today = date.today()
        if obj.birth_date is None:
            return None
        return today.year - obj.birth_date.year - (
                (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
