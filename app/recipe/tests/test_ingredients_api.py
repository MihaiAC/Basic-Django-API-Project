"""
Tests for the Ingredient API.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse("recipe:ingredient-list")


def detail_url(ingredient_id):
    """Create and return a tag detail URL."""
    return reverse("recipe:ingredient-detail", args=[ingredient_id])


def create_user(email="user@example.com", password="password123"):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class PublicIngredientsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving tags."""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving a list of tags."""
        Ingredient.objects.create(user=self.user, name="ing1")
        Ingredient.objects.create(user=self.user, name="ing2")

        res = self.client.get(INGREDIENTS_URL)

        ingredient = Ingredient.objects.all().order_by("-name")

        serializer = IngredientSerializer(ingredient, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that list of tags is limited to authenticated user."""
        user2 = create_user(email="user2@example.com")
        Ingredient.objects.create(user=user2, name="ing1")

        ingredient = Ingredient.objects.create(user=self.user, name="Comfort Food")
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)
        self.assertEqual(res.data[0]["id"], ingredient.id)

    # def test_update_tag(self):
    #     """Test updating a tag."""
    #     tag = Tag.objects.create(user=self.user, name="After Dinner")

    #     payload = {"name": "Dessert"}
    #     url = detail_url(tag.id)
    #     res = self.client.patch(url, payload)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     tag.refresh_from_db()
    #     self.assertEqual(tag.name, payload["name"])

    # def test_delete_tag(self):
    #     """Test deleting a tag."""
    #     tag = Tag.objects.create(user=self.user, name="After Dinner")

    #     url = detail_url(tag.id)
    #     res = self.client.delete(url)

    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #     tags = Tag.objects.filter(user=self.user)
    #     self.assertFalse(tags.exists())
