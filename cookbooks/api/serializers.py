from django.contrib.auth import get_user_model
from rest_framework import serializers

from cookbooks.models import Cookbook, Ingredient, Instruction, Recipe

User = get_user_model()


class ReadonlyInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = "order", "action", "tip"


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        exclude = "id", "recipe"


class ReadonlyIngredientSerializer(serializers.ModelSerializer):
    amount_unit = serializers.SerializerMethodField("amount_unit_name")

    def amount_unit_name(self, obj):
        return list(filter(lambda u: u[0] == obj.amount_unit, Ingredient.AMOUNT_UNIT_CHOICES))[0][
            1
        ]

    class Meta:
        model = Ingredient
        fields = "name", "amount", "amount_unit"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        exclude = "id", "recipe"


class ReadonlyRecipeSerializer(serializers.ModelSerializer):
    ingredients = ReadonlyIngredientSerializer(many=True)
    instructions = ReadonlyInstructionSerializer(many=True)
    difficulty = serializers.SerializerMethodField("difficulty_name")
    created_by = serializers.ReadOnlyField(source=f"created_by.{User.USERNAME_FIELD}")

    def difficulty_name(self, obj):
        return list(filter(lambda d: d[0] == obj.difficulty, Recipe.DIFFICULTY_CHOICES))[0][1]

    class Meta:
        model = Recipe
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    instructions = InstructionSerializer(many=True)

    class Meta:
        model = Recipe
        exclude = ("created_by",)

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        instructions = validated_data.pop("instructions")
        created_by = self.context["request"].user

        recipe = Recipe.objects.create(**(validated_data | {"created_by": created_by}))

        ingredients = [
            Ingredient(**(ingredient_data | {"recipe": recipe})) for ingredient_data in ingredients
        ]
        ingredients = Ingredient.objects.bulk_create(ingredients)
        recipe.ingredients.add(*ingredients)

        # override ordering by 1, 2, 3...
        instructions = [
            Instruction(**(instruction_data | {"recipe": recipe, "order": order}))
            for order, instruction_data in enumerate(instructions, start=1)
        ]
        instructions = Instruction.objects.bulk_create(instructions)
        recipe.instructions.add(*instructions)

        return recipe


class ReadonlyCookbookSerializer(serializers.ModelSerializer):
    recipes = ReadonlyRecipeSerializer(many=True)
    recipes_count = serializers.IntegerField()

    class Meta:
        model = Cookbook
        fields = "id", "recipes_count", "recipes"
