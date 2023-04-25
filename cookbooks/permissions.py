from django.shortcuts import get_object_or_404
from rest_framework import permissions

from .models import Recipe


class IsRecipeCreatorOrAdminPermission(permissions.IsAdminUser):
    def has_permission(self, request, view):
        recipe_id = request.parser_context["kwargs"]["pk"]
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        return request._user == recipe.created_by or request._user.is_staff
