from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .client_serializers import ClientSerializer


class LogInSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = ClientSerializer(user).data
        for key, value in user_data.items():
            if key != "id":
                token[key] = value
        return token


class LogInResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField(label="Refresh Token")
    access = serializers.CharField(label="Access Token")
