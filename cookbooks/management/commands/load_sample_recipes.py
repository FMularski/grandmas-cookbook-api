from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from cookbooks.models import Cookbook, Ingredient, Instruction, Recipe

User = get_user_model()


class Command(BaseCommand):
    help = "Load sample recipes."

    def handle(self, *args, **options):
        if Recipe.objects.exists():
            return self.stdout.write(
                self.style.WARNING("Some recipes already exists. Aborting loading sample recipes.")
            )

        cookbooks = Cookbook.objects.all()
        # recipe # 1
        recipe1 = Recipe.objects.create(
            created_by=User.objects.first(),
            title="Pizza with homemade sauce",
            description="Simple recipe for a tasty pizza.",
            difficulty="E",
            rating=4.5,
        )
        Ingredient.objects.bulk_create(
            [
                Ingredient(recipe=recipe1, name="flour", amount=300, amount_unit="G"),
                Ingredient(recipe=recipe1, name="olive oil", amount=1, amount_unit="T"),
                Ingredient(recipe=recipe1, name="passata", amount=200, amount_unit="M"),
                Ingredient(recipe=recipe1, name="mozarella", amount=8, amount_unit="U"),
            ]
        )
        Instruction.objects.bulk_create(
            [
                Instruction(
                    recipe=recipe1,
                    order=1,
                    action="Tip the flour into a bowl, then stir in the yeast and 1 tsp salt.",
                ),
                Instruction(
                    recipe=recipe1,
                    order=2,
                    action="Make a well in the centre and pour in 200ml water along with the oil.",
                ),
                Instruction(
                    recipe=recipe1,
                    order=3,
                    action="Stir together with a spoon until you have a soft and wet dough.",
                ),
            ]
        )

        for cookbook in cookbooks:
            cookbook.recipes.add(recipe1)

        self.stdout.write(self.style.SUCCESS("Cookbooks loaded."))
