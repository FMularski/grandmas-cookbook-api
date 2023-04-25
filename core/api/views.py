from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import TokenAPIViewResponseSerializer, TokenRefreshAPIViewResponseSerializer

"""
    Overriding views for custom swagger documentation
"""


class TokenAPIView(TokenObtainPairView):
    token_apiview_description = """
        Returns JWT tokens and custom user's type.

        Credentials for testing purposes:
        * e: admin@mail.com p: admin (SU)
        * e: golden@mail.com p: golden
        * e: silver@mail.com p: silver
        * e: bronze@mail.com p: bronze
    """

    @swagger_auto_schema(
        operation_description=token_apiview_description,
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
