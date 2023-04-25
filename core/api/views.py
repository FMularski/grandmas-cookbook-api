from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import TokenAPIViewResponseSerializer, TokenRefreshAPIViewResponseSerializer

"""
    Overriding views for custom swagger documentation
"""


class TokenAPIView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_description="Returns JWT tokens and custom user's type.",
        responses={status.HTTP_200_OK: TokenAPIViewResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshAPIView(TokenRefreshView):
    @swagger_auto_schema(
        operation_description="Returns refreshed access token.",
        responses={status.HTTP_200_OK: TokenRefreshAPIViewResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
