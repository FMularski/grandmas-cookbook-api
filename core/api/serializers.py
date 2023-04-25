from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        type = list(filter(lambda t: t[0] == self.user.type, self.user.TYPE_CHOICES))[0][1]
        data["type"] = type

        return data


"""
    Serializers used just for documentation
"""


class TokenAPIViewResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    type = serializers.CharField()


class TokenRefreshAPIViewResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
