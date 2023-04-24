from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from .models import Cookbook, Ingredient, Instruction, Recipe


class CookbookAdmin(ModelAdmin):
    list_display = "user", "recipes_count"


class IngredientInline(TabularInline):
    model = Ingredient
    fields = "name", "amount", "amount_unit"
    extra = 0


class InstructionInline(TabularInline):
    model = Instruction
    ordering = ("order",)
    fields = "order", "action", "tip"
    extra = 0


class RecipeAdmin(ModelAdmin):
    list_display = "title", "created_by", "difficulty", "rating"
    ordering = ("-rating",)
    inlines = IngredientInline, InstructionInline


admin.site.register(Cookbook, CookbookAdmin)
admin.site.register(Recipe, RecipeAdmin)
