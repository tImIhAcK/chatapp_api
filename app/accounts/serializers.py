from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username
        token['is_active'] = user.is_active
        # ...

        return token


class UserSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['username', 'email']

    def create(self, validated_data):
        user = User(**validated_data)

        email_sent = user.send_activation_email()

        if email_sent:
            return Response(status=status.HTTP_201_CREATED)

        return Response(
            {"message": "Failed to send activation email."},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user',
            'first_name',
            'last_name',
            'gender'
            'phone',
            'address'
            'city',
            'state',
            'country',
            'avatar',
            'bio'

        ]

    def create(self, validated_data, *args, **kwargs):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data, *args, **kwargs)
