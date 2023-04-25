from rest_framework import generics

from cookbooks.models import Recipe

from .serializers import RecipeSerializer


class RecipeListAPIView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
