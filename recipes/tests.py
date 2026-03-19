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

    def test_signup_redirects_to_homepage(self):
        response = self.client.post(
            reverse("recipes:signup"),
            {
                "username": "redirectuser",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/homepage/")

    def test_signup_logs_user_in(self):
        self.client.post(
            reverse("recipes:signup"),
            {
                "username": "autologinuser",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        response = self.client.get(reverse("recipes:myrecipes"))
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials_redirects_to_homepage(self):
        User.objects.create_user(username="loginuser", password="StrongPass123!")

        response = self.client.post(
            reverse("recipes:login"),
            {
                "username": "loginuser",
                "password": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/homepage/")

    def test_login_with_invalid_credentials_shows_error(self):
        User.objects.create_user(username="wrongpassuser", password="StrongPass123!")

        response = self.client.post(
            reverse("recipes:login"),
            {
                "username": "wrongpassuser",
                "password": "WrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password.")

    def test_logged_out_user_is_redirected_from_my_recipes(self):
        response = self.client.get(reverse("recipes:myrecipes"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("recipes:login"), response.url)

    def test_logged_in_user_can_access_my_recipes(self):
        User.objects.create_user(username="testuser", password="StrongPass123!")
        self.client.login(username="testuser", password="StrongPass123!")

        response = self.client.get(reverse("recipes:myrecipes"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have 0 recipe(s).")

    def test_logged_out_user_is_redirected_from_create_recipe(self):
        response = self.client.get(reverse("recipes:createrecipe"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("recipes:login"), response.url)

    def test_logged_in_user_can_create_recipe_with_author(self):
        user = User.objects.create_user(username="recipeuser", password="StrongPass123!")
        self.client.login(username="recipeuser", password="StrongPass123!")

        response = self.client.post(
            reverse("recipes:createrecipe"),
            {
                "name": "Soup",
                "description": "Warm soup",
                "cuisine": "other",
                "difficulty": "easy",
                "cooking_time": 15,
                "ingredients": "Water, vegetables",
                "instructions": "Boil and serve",
            },
        )

        self.assertEqual(response.status_code, 302)
        recipe = Recipes.objects.get(name="Soup")
        self.assertEqual(recipe.author, user)
        self.assertEqual(response.url, reverse("recipes:recipe_detail", args=[recipe.id]))

    def test_logout_redirects_to_homepage(self):
        User.objects.create_user(username="logoutuser", password="StrongPass123!")
        self.client.login(username="logoutuser", password="StrongPass123!")

        response = self.client.get(reverse("recipes:logout"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/homepage/")

    def test_homepage_search_returns_matching_recipes(self):
        user = User.objects.create_user(username="searchuser", password="StrongPass123!")

        Recipes.objects.create(
            author=user,
            name="Pizza",
            description="Cheesy pizza",
            cuisine="italian",
            difficulty="easy",
            cooking_time=20,
            ingredients="Dough, cheese, tomato sauce",
            instructions="Bake the pizza",
        )

        Recipes.objects.create(
            author=user,
            name="Curry",
            description="Spicy curry",
            cuisine="indian",
            difficulty="medium",
            cooking_time=40,
            ingredients="Chicken, curry paste",
            instructions="Cook and serve",
        )

        response = self.client.get(reverse("recipes:homepage"), {"q": "pizza"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pizza")
        self.assertNotContains(response, "Curry")
