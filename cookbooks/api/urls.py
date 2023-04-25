from django.urls import path

from .views import RecipeListAPIView

urlpatterns = [
    path("recipes/", RecipeListAPIView.as_view(), name="recipes"),
]
