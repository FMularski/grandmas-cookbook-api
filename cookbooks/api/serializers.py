from django.contrib.auth import get_user_model
from rest_framework import serializers

from cookbooks.models import Cookbook, Ingredient, Instruction, Recipe

User = get_user_model()


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = "order", "action", "tip"


class IngredientSerializer(serializers.ModelSerializer):
    amount_unit = serializers.SerializerMethodField("amount_unit_name")

    def amount_unit_name(self, obj):
        return list(filter(lambda u: u[0] == obj.amount_unit, Ingredient.AMOUNT_UNIT_CHOICES))[0][
            1
        ]

    class Meta:
        model = Ingredient
        fields = "name", "amount", "amount_unit"


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    instructions = InstructionSerializer(many=True)
    difficulty = serializers.SerializerMethodField("difficulty_name")
    created_by = serializers.ReadOnlyField(source=f"created_by.{User.USERNAME_FIELD}")

    def difficulty_name(self, obj):
        return list(filter(lambda d: d[0] == obj.difficulty, Recipe.DIFFICULTY_CHOICES))[0][1]

    class Meta:
        model = Recipe
        fields = "__all__"


class CookbookSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True)
    recipes_count = serializers.IntegerField()

    class Meta:
        model = Cookbook
        fields = "id", "recipes_count", "recipes"
