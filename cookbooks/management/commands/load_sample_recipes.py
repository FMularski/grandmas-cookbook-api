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

        if not User.objects.exists():
            return self.stdout.write(
                self.style.ERROR("At least one existing user object is required.")
            )

        # recipe no. 1
        recipe1 = Recipe.objects.create(
            created_by=User.objects.last(),
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
                    tip="You can use a cup to make the well.",
                ),
                Instruction(
                    recipe=recipe1,
                    order=3,
                    action="Stir together with a spoon until you have a soft and wet dough.",
                    tip="Avoid making the dough to wet.",
                ),
            ]
        )

        # recipe no. 2
        recipe2 = Recipe.objects.create(
            created_by=User.objects.last(),
            title="Lemon & yogurt chicken flatbreads",
            description="Fast recipe for a juicy chicken.",
            difficulty="M",
            rating=4.2,
        )
        Ingredient.objects.bulk_create(
            [
                Ingredient(recipe=recipe2, name="chicken breasts", amount=2, amount_unit="U"),
                Ingredient(recipe=recipe2, name="greek yoghurt", amount=4, amount_unit="T"),
                Ingredient(recipe=recipe2, name="lemons", amount=1, amount_unit="U"),
                Ingredient(recipe=recipe2, name="flatbreads", amount=4, amount_unit="U"),
            ]
        )
        Instruction.objects.bulk_create(
            [
                Instruction(
                    recipe=recipe2,
                    order=1,
                    action="Put the chicken in a bowl. Pare strips of zest from the lemon.",
                ),
                Instruction(
                    recipe=recipe2,
                    order=2,
                    action="Heat the barbecue. If using coals, wait until they turn white.",
                ),
                Instruction(
                    recipe=recipe2,
                    order=3,
                    action="Warm the flatbreads on the edge of the barbecue for a minute.",
                    tip="Do not keep the meet too long on the barbecue as it may dry out.",
                ),
                Instruction(
                    recipe=recipe2,
                    order=4,
                    action="Fold or roll the flatbreads to eat.",
                ),
            ]
        )

        # recipe no. 3
        recipe3 = Recipe.objects.create(
            created_by=User.objects.last(),
            title="Rice paper rolls",
            description="Make these rice paper wraps for an easy snack or appetizer.",
            difficulty="E",
            rating=3.9,
        )
        Ingredient.objects.bulk_create(
            [
                Ingredient(recipe=recipe3, name="rice noodles", amount=50, amount_unit="G"),
                Ingredient(recipe=recipe3, name="peeled avocado", amount=1, amount_unit="U"),
                Ingredient(recipe=recipe3, name="rice paper wraps", amount=8, amount_unit="U"),
                Ingredient(recipe=recipe3, name="sweet chilli sauce", amount=2, amount_unit="T"),
                Ingredient(recipe=recipe3, name="carrots", amount=1, amount_unit="U"),
            ]
        )
        Instruction.objects.bulk_create(
            [
                Instruction(
                    recipe=recipe3,
                    order=1,
                    action="Put the noodles in a pan of water and bring to the boil.",
                ),
                Instruction(
                    recipe=recipe3,
                    order=2,
                    action="Heat the barbecue and wait until the coals turn white.",
                ),
                Instruction(
                    recipe=recipe3,
                    order=3,
                    action="Cut the carrot into matchsticks using a knife or a mandoline.",
                    tip="You can also chop it if you like.",
                ),
                Instruction(
                    recipe=recipe3,
                    order=4,
                    action="Lift 1 sheet of rice paper out of the water, shake gently.",
                ),
            ]
        )

        # recipe no. 4
        recipe4 = Recipe.objects.create(
            created_by=User.objects.last(),
            title="Salmon & spaghetti supper in a parcel",
            description="Create a bit of fun for kids by serving supper in a parcel.",
            difficulty="H",
            rating=4.1,
        )
        Ingredient.objects.bulk_create(
            [
                Ingredient(recipe=recipe4, name="spaghetti", amount=200, amount_unit="G"),
                Ingredient(recipe=recipe4, name="salmon fillets", amount=4, amount_unit="U"),
                Ingredient(recipe=recipe4, name="cherry tomatoes", amount=100, amount_unit="G"),
                Ingredient(recipe=recipe4, name="garlic clove", amount=1, amount_unit="U"),
            ]
        )
        Instruction.objects.bulk_create(
            [
                Instruction(
                    recipe=recipe4,
                    order=1,
                    action="Cook the spaghetti following pack instructions and drain.",
                ),
                Instruction(
                    recipe=recipe4,
                    order=2,
                    action="Divide the spaghetti between the pieces of parchment.",
                ),
                Instruction(
                    recipe=recipe4,
                    order=3,
                    action="Heat the oil and fry the garlic for 1 min.",
                    tip="Put on the lid to fasten the process.",
                ),
                Instruction(
                    recipe=recipe4,
                    order=4,
                    action="Serve each person a puffed parcel in a shallow bowl.",
                    tip="You can sprinkle the spaghetti with a lemon juice.",
                ),
            ]
        )

        for cookbook in Cookbook.objects.all():
            cookbook.recipes.add(recipe1)
            cookbook.recipes.add(recipe2)
            cookbook.recipes.add(recipe3)
            cookbook.recipes.add(recipe4)

        self.stdout.write(self.style.SUCCESS("Recipes loaded."))
