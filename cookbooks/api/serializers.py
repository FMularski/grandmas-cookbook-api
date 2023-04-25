import itertools

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _
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

    def _update_ingredients(self, instance, ingredients_data):
        ingredients_db = instance.ingredients.all()
        # iterate over zipped collection, check on which side (data or db) the object is missing,
        # even => update in parallel;
        # missing on db => need more db; missing on data => need less db
        for ingredient_data, ingredient_db in itertools.zip_longest(
            ingredients_data, ingredients_db
        ):
            if ingredient_data and ingredient_db:
                Ingredient.objects.filter(pk=ingredient_db.pk).update(**ingredient_data)
                continue
            if ingredient_data and not ingredient_db:
                # check when PATCH with insufficient fields data
                try:
                    Ingredient.objects.create(**(ingredient_data | {"recipe": instance}))
                except IntegrityError:
                    raise serializers.ValidationError(_("Insufficient data."))
                finally:
                    continue
            if not ingredient_data and ingredient_db:
                ingredient_db.delete()

    def _update_instructions(self, instance, instructions_data):
        instructions_db = instance.instructions.all()
        # same logic as in _update_ingredients
        for instruction_data, instruction_db in itertools.zip_longest(
            instructions_data, instructions_db
        ):
            if instruction_data and instruction_db:
                Instruction.objects.filter(pk=instruction_db.pk).update(**instruction_data)
                continue
            if instruction_data and not instruction_db:
                try:
                    Instruction.objects.create(**(instruction_data | {"recipe": instance}))
                except IntegrityError:
                    raise serializers.ValidationError(_("Insufficient data."))
                finally:
                    continue
            if not instruction_data and instruction_db:
                instruction_db.delete()

    def update(self, instance, validated_data):
        if "ingredients" in validated_data:
            ingredients = validated_data.pop("ingredients")
            self._update_ingredients(instance, ingredients)
        if "instructions" in validated_data:
            instructions = validated_data.pop("instructions")
            self._update_instructions(instance, instructions)

        Recipe.objects.filter(pk=instance.pk).update(**validated_data)
        return Recipe.objects.get(pk=instance.pk)


class ReadonlyCookbookSerializer(serializers.ModelSerializer):
    recipes = ReadonlyRecipeSerializer(many=True)
    recipes_count = serializers.IntegerField()

    class Meta:
        model = Cookbook
        fields = "id", "recipes_count", "recipes"
