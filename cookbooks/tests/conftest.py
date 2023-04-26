import pytest
from pytest_factoryboy import register

from .factories import IngredientFactory, InstructionFactory, RecipeFactory, UserFactory


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


register(UserFactory)
register(IngredientFactory)
register(InstructionFactory)
register(RecipeFactory)
