from django.urls import path

from .views import MyCookbookAPIView, RecipeListAPIView, RecipeRetrieveAPIView

urlpatterns = [
    path("recipes/", RecipeListAPIView.as_view(), name="recipes"),
    path("recipes/<pk>/", RecipeRetrieveAPIView.as_view(), name="recipe"),
    path("my-cookbook/", MyCookbookAPIView.as_view(), name="my-cookbook"),
]
