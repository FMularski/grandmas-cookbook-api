import pytest
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from rest_framework import status

from cookbooks.models import Cookbook, Ingredient, Instruction, Recipe

User = get_user_model()

"""
    Models creation tests.
"""


@pytest.mark.django_db
def test_create_user(user_factory):
    assert User.objects.count() == 0
    user_factory()
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_create_cookbook_signal(user_factory):
    assert Cookbook.objects.count() == 0
    user_factory()
    assert Cookbook.objects.count() == 1


@pytest.mark.django_db
def test_create_ingredient(ingredient_factory):
    assert Ingredient.objects.count() == 0
    ingredient_factory()
    assert Ingredient.objects.count() == 1


@pytest.mark.django_db
def test_create_instruction(instruction_factory):
    assert Instruction.objects.count() == 0
    instruction_factory()
    assert Instruction.objects.count() == 1


@pytest.mark.django_db
def test_create_recipe(recipe_factory):
    assert Recipe.objects.count() == 0
    recipe_factory()
    assert Recipe.objects.count() == 1


"""
    Public endpoints tests.
"""


@pytest.mark.django_db
def test_get_recipes(api_client, recipe_factory):
    url = reverse("recipes")
    response = api_client.get(url)
    recipe_factory()
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_recipe_id(api_client, recipe_factory):
    recipe = recipe_factory()
    url = reverse("recipe", kwargs={"pk": recipe.pk})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


"""
    Private endpoints tests.
"""


@pytest.mark.django_db
def test_token(api_client, user_factory):
    user = user_factory()
    url = reverse("token")
    response = api_client.post(url, data={"email": user.email, "password": "password"})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_custom_type(api_client, user_factory):
    default_user_type = "Bronze"
    user = user_factory()
    url = reverse("token")
    response = api_client.post(url, data={"email": user.email, "password": "password"}).json()
    assert "type" in response
    assert response["type"] == default_user_type


@pytest.mark.django_db
def test_get_mycookbook(api_client, user_factory):
    user = user_factory()
    token_url = reverse("token")
    access_token = api_client.post(
        token_url, data={"email": user.email, "password": "password"}
    ).json()["access"]

    mycookbook_url = reverse("my-cookbook")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = api_client.get(mycookbook_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_su, response_status", ([True, status.HTTP_201_CREATED], [False, status.HTTP_403_FORBIDDEN])
)
def test_post_recipes(api_client, user_factory, is_su, response_status):
    user = user_factory(is_staff=is_su, is_superuser=is_su)
    token_url = reverse("token")
    access_token = api_client.post(
        token_url, data={"email": user.email, "password": "password"}
    ).json()["access"]

    recipes_url = reverse("recipes")
    body = {
        "ingredients": [{"name": "ingredient 1", "amount": 100, "amount_unit": "M"}],
        "instructions": [{"order": 1, "action": "instruction 1", "tip": "tip 1"}],
        "title": "title 1",
        "description": "desc 1",
        "difficulty": "E",
        "rating": 4.5,
    }

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = api_client.post(recipes_url, data=body, format="json")
    assert response.status_code == response_status


@pytest.mark.django_db
def test_delete_recipe_id(api_client, recipe_factory):
    recipe = recipe_factory()

    user = recipe.created_by
    token_url = reverse("token")
    access_token = api_client.post(
        token_url, data={"email": user.email, "password": "password"}
    ).json()["access"]

    delete_url = reverse("recipe", kwargs={"pk": recipe.pk})

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = api_client.delete(delete_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
@pytest.mark.parametrize(
    "text, diff, rating, response_status",
    (
        ["updated", "E", 2.5, status.HTTP_200_OK],
        ["some other text", "M", 3.75, status.HTTP_200_OK],
        ["yet another text", "H", 5, status.HTTP_200_OK],
        ["updated", "invalid difficulty", 5, status.HTTP_400_BAD_REQUEST],
        ["updated", "H", -1, status.HTTP_400_BAD_REQUEST],
        [None, "E", 2.5, status.HTTP_400_BAD_REQUEST],
    ),
)
def test_put_recipe_id(api_client, recipe_factory, text, diff, rating, response_status):
    recipe = recipe_factory()

    user = recipe.created_by
    token_url = reverse("token")
    access_token = api_client.post(
        token_url, data={"email": user.email, "password": "password"}
    ).json()["access"]

    put_url = reverse("recipe", kwargs={"pk": recipe.pk})
    body = {
        "ingredients": [{"name": text, "amount": 100, "amount_unit": "M"}],
        "instructions": [{"order": 1, "action": text, "tip": "tip 1"}],
        "title": text,
        "description": text,
        "difficulty": diff,
        "rating": rating,
    }

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = api_client.put(put_url, data=body, format="json")

    assert response.status_code == response_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "text, diff, rating, response_status",
    (
        ["updated", "E", 2.5, status.HTTP_200_OK],
        ["some other text", "M", 3.75, status.HTTP_200_OK],
        ["yet another text", "H", 5, status.HTTP_200_OK],
        ["updated", "invalid difficulty", 5, status.HTTP_400_BAD_REQUEST],
        ["updated", "H", -1, status.HTTP_400_BAD_REQUEST],
        [None, "E", 2.5, status.HTTP_400_BAD_REQUEST],
    ),
)
def test_patch_recipe_id(api_client, recipe_factory, text, diff, rating, response_status):
    recipe = recipe_factory()

    user = recipe.created_by
    token_url = reverse("token")
    access_token = api_client.post(
        token_url, data={"email": user.email, "password": "password"}
    ).json()["access"]

    patch_url = reverse("recipe", kwargs={"pk": recipe.pk})
    body = {
        "ingredients": [
            {
                "name": text,
                "amount": 100,
            },
            {
                "name": text,
                "amount": 200,
            },
        ],
        "instructions": [
            {
                "action": text,
            },
            {"action": text},
        ],
        "difficulty": diff,
        "rating": rating,
    }

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = api_client.patch(patch_url, data=body, format="json")

    assert response.status_code == response_status
