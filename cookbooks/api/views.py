from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from cookbooks.models import Recipe

from .serializers import RecipeSerializer


class RecipeListAPIView(generics.ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        order = self.request.GET.get("order")
        return Recipe.objects.all().order_by(f"-{order}") if order else Recipe.objects.all()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "order", openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=["rating", "created_at"]
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
