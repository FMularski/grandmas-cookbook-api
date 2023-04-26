import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from faker import Faker

from cookbooks.models import Ingredient, Instruction, Recipe

User = get_user_model()
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = fake.email()
    password = make_password("password")
    is_active = True
    is_staff = True


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    created_by = factory.SubFactory(UserFactory)

    title = fake.name()
    description = fake.text()
    difficulty = "E"
    rating = 4.5


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    recipe = factory.SubFactory(RecipeFactory)

    name = fake.name()
    amount = 1
    amount_unit = "M"


class InstructionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Instruction

    recipe = factory.SubFactory(RecipeFactory)

    action = fake.name()
    order = 1
