from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Recipes


class RecipeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ismailtest", password="StrongPass123!")

    def test_recipe_string_representation_returns_name(self):
        recipe = Recipes.objects.create(
            author=self.user,
            name="Pasta",
            description="Simple pasta dish",
            cuisine="italian",
            difficulty="easy",
            cooking_time=20,
            ingredients="Pasta, sauce",
            instructions="Boil pasta and add sauce",
        )

        self.assertEqual(str(recipe), "Pasta")

    def test_recipe_is_linked_to_author(self):
        recipe = Recipes.objects.create(
            author=self.user,
            name="Curry",
            description="Spicy curry",
            cuisine="indian",
            difficulty="medium",
            cooking_time=40,
            ingredients="Chicken, curry paste",
            instructions="Cook chicken and add curry paste",
        )

        self.assertEqual(recipe.author, self.user)


class AuthViewTest(TestCase):
    def test_signup_page_loads(self):
        response = self.client.get(reverse("recipes:signup"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_sign_up(self):
        response = self.client.post(
            reverse("recipes:signup"),
            {
                "username": "newuser",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_logged_out_user_is_redirected_from_my_recipes(self):
        response = self.client.get(reverse("recipes:myrecipes"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("recipes:login"), response.url)

    def test_logged_in_user_can_access_my_recipes(self):
        user = User.objects.create_user(username="testuser", password="StrongPass123!")
        self.client.login(username="testuser", password="StrongPass123!")

        response = self.client.get(reverse("recipes:myrecipes"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have 0 recipe(s).")

    def test_logout_redirects_to_homepage(self):
        user = User.objects.create_user(username="logoutuser", password="StrongPass123!")
        self.client.login(username="logoutuser", password="StrongPass123!")

        response = self.client.get(reverse("recipes:logout"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/homepage/")
