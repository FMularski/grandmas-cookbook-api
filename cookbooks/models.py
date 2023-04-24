from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def validate_between_0_and_5(value):
    if value < 0 or value > 5:
        raise ValidationError(_("Value must be a number between 0 and 5."))


def validate_greater_than_0(value):
    if value < 0:
        raise ValidationError(_("Value must be greater than 0."))


class Recipe(models.Model):
    DIFFICULTY_EASY = "E"
    DIFFICULTY_MEDIUM = "M"
    DIFFICULTY_HARD = "H"

    DIFFICULTY_CHOICES = (
        (DIFFICULTY_EASY, _("Easy")),
        (DIFFICULTY_MEDIUM, _("Medium")),
        (DIFFICULTY_HARD, _("Hard")),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_recipes")
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    difficulty = models.CharField(
        max_length=1, choices=DIFFICULTY_CHOICES, default=DIFFICULTY_EASY
    )
    rating = models.FloatField(default=0, validators=[validate_between_0_and_5])


class Cookbook(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cookbook")
    recipes = models.ManyToManyField(Recipe, related_name="cookbooks")

    @property
    def recipes_count(self):
        return self.cookbooks.all().count()

    def __str__(self):
        return _(f"{self.user}'s cookbook")


class Ingredient(models.Model):
    AMOUNT_UNIT_ML = "M"
    AMOUNT_UNIT_G = "G"
    AMOUNT_UNIT_TABLESPOON = "T"
    AMOUNT_UNIT_CUP = "C"
    AMOUNT_UNIT_UNIT = "U"

    AMOUNT_UNIT_CHOICES = (
        (AMOUNT_UNIT_ML, _("ml")),
        (AMOUNT_UNIT_G, _("g")),
        (AMOUNT_UNIT_TABLESPOON, _("tablespoons")),
        (AMOUNT_UNIT_CUP, _("cups")),
        (AMOUNT_UNIT_UNIT, _("units")),
    )

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    name = models.CharField(max_length=100)
    amount = models.FloatField(validators=[validate_greater_than_0])
    amount_unit = models.CharField(max_length=1, choices=AMOUNT_UNIT_CHOICES)

    def __str__(self):
        return f"{self.name} [{self.amount} {self.amount_unit}]"


class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="instructions")
    order = models.PositiveSmallIntegerField()
    action = models.CharField(max_length=200)
    tip = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ("order",)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.order is None:
            last_instruction = self.recipe.instructions.last()
            self.order = last_instruction.order + 1 if last_instruction else 1
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"[{self.recipe}]: {self.action}"
