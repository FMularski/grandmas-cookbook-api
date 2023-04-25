from django.urls import path

from .views import MyCookbookAPIView, RecipeListAPIView

urlpatterns = [
    path("recipes/", RecipeListAPIView.as_view(), name="recipes"),
    path("my-cookbook/", MyCookbookAPIView.as_view(), name="my-cookbook"),
]
