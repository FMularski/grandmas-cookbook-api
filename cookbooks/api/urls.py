from django.urls import path

from .views import MyCookbookAPIView, RecipeDetailAPIView, RecipeListAPIView

urlpatterns = [
    path("recipes/", RecipeListAPIView.as_view(), name="recipes"),
    path("recipes/<pk>/", RecipeDetailAPIView.as_view(), name="recipe"),
    path("my-cookbook/", MyCookbookAPIView.as_view(), name="my-cookbook"),
]
