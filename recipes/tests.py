import io
import os
import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Recipes, Rating, SavedRecipe


# Basic model tests for the Recipes model.
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


# Tests for signup, login, logout, access control, and homepage search.
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

    def test_logged_in_user_is_redirected_away_from_login_page(self):
        User.objects.create_user(username="alreadyin", password="StrongPass123!")
        self.client.login(username="alreadyin", password="StrongPass123!")

        response = self.client.get(reverse("recipes:login"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/homepage/")

    def test_logged_in_user_is_redirected_away_from_signup_page(self):
        User.objects.create_user(username="signedin", password="StrongPass123!")
        self.client.login(username="signedin", password="StrongPass123!")

        response = self.client.get(reverse("recipes:signup"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/homepage/")

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
        self.assertTemplateUsed(response, "viewcategory.html")

    def test_logged_out_user_is_redirected_from_create_recipe(self):
        response = self.client.get(reverse("recipes:createrecipe"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("recipes:login"), response.url)

    def test_logged_out_user_cannot_access_saved_recipes_page(self):
        response = self.client.get(reverse("recipes:saved"))

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


# Tests for recipe form validation, text length limits, and invalid uploads.
class RecipeValidationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="validationuser", password="StrongPass123!")
        self.client.login(username="validationuser", password="StrongPass123!")

    def test_create_recipe_rejects_cooking_time_below_minimum(self):
        response = self.client.post(
            reverse("recipes:createrecipe"),
            {
                "name": "Invalid Soup",
                "description": "Test description",
                "cuisine": "other",
                "difficulty": "easy",
                "cooking_time": 0,
                "ingredients": "Water\nVegetables",
                "instructions": "Boil\nServe",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recipes.objects.filter(name="Invalid Soup").exists())
        self.assertContains(response, "Cooking time must be at least 1 minute.")

    def test_create_recipe_rejects_cooking_time_above_maximum(self):
        response = self.client.post(
            reverse("recipes:createrecipe"),
            {
                "name": "Endless Stew",
                "description": "Test description",
                "cuisine": "other",
                "difficulty": "easy",
                "cooking_time": 1441,
                "ingredients": "Water\nVegetables",
                "instructions": "Boil\nServe",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recipes.objects.filter(name="Endless Stew").exists())
        self.assertContains(response, "Cooking time cannot exceed 1440 minutes.")

    def test_create_recipe_rejects_blank_name(self):
        response = self.client.post(
            reverse("recipes:createrecipe"),
            {
                "name": "   ",
                "description": "Test description",
                "cuisine": "other",
                "difficulty": "easy",
                "cooking_time": 15,
                "ingredients": "Water\nVegetables",
                "instructions": "Boil\nServe",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Recipes.objects.count(), 0)
        self.assertContains(response, "Name: This field is required.")

    def test_create_recipe_rejects_blank_ingredients(self):
        response = self.client.post(
            reverse("recipes:createrecipe"),
            {
                "name": "Soup",
                "description": "Test description",
                "cuisine": "other",
                "difficulty": "easy",
                "cooking_time": 15,
                "ingredients": "   ",
                "instructions": "Boil\nServe",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recipes.objects.filter(name="Soup").exists())
        self.assertContains(response, "Ingredients: This field is required.")

    def test_create_recipe_rejects_blank_instructions(self):
        response = self.client.post(
            reverse("recipes:createrecipe"),
            {
                "name": "Soup",
                "description": "Test description",
                "cuisine": "other",
                "difficulty": "easy",
                "cooking_time": 15,
                "ingredients": "Water\nVegetables",
                "instructions": "   ",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recipes.objects.filter(name="Soup").exists())
        self.assertContains(response, "Instructions: This field is required.")

    def test_create_recipe_rejects_description_over_300_characters(self):
        response = self.client.post(
            reverse("recipes:createrecipe"),
            {
                "name": "Long Description Recipe",
                "description": "a" * 301,
                "cuisine": "other",
                "difficulty": "easy",
                "cooking_time": 15,
                "ingredients": "Water\nVegetables",
                "instructions": "Boil\nServe",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recipes.objects.filter(name="Long Description Recipe").exists())
        self.assertContains(response, "Description cannot be longer than 300 characters.")

    def test_create_recipe_rejects_ingredients_over_2000_characters(self):
        response = self.client.post(
            reverse("recipes:createrecipe"),
            {
                "name": "Long Ingredients Recipe",
                "description": "Valid description",
                "cuisine": "other",
                "difficulty": "easy",
                "cooking_time": 15,
                "ingredients": "a" * 2001,
                "instructions": "Boil\nServe",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recipes.objects.filter(name="Long Ingredients Recipe").exists())
        self.assertContains(response, "Ingredients cannot be longer than 2000 characters.")

    def test_create_recipe_rejects_instructions_over_3000_characters(self):
        response = self.client.post(
            reverse("recipes:createrecipe"),
            {
                "name": "Long Instructions Recipe",
                "description": "Valid description",
                "cuisine": "other",
                "difficulty": "easy",
                "cooking_time": 15,
                "ingredients": "Water\nVegetables",
                "instructions": "a" * 3001,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recipes.objects.filter(name="Long Instructions Recipe").exists())
        self.assertContains(response, "Instructions cannot be longer than 3000 characters.")

    def test_create_recipe_rejects_non_image_upload(self):
        fake_file = SimpleUploadedFile(
            "not_an_image.jpg",
            b"this is not a real image",
            content_type="image/jpeg",
        )

        response = self.client.post(
            reverse("recipes:createrecipe"),
            {
                "name": "Bad Upload Recipe",
                "description": "Valid description",
                "cuisine": "other",
                "difficulty": "easy",
                "cooking_time": 15,
                "ingredients": "Water\nVegetables",
                "instructions": "Boil\nServe",
                "image": fake_file,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recipes.objects.filter(name="Bad Upload Recipe").exists())
        self.assertContains(response, "Upload a valid image")

    def test_create_recipe_rejects_gif_upload(self):
        image_buffer = io.BytesIO()
        image = Image.new("RGB", (10, 10), "white")
        image.save(image_buffer, format="GIF")
        image_buffer.seek(0)

        gif_file = SimpleUploadedFile(
            "test.gif",
            image_buffer.getvalue(),
            content_type="image/gif",
        )

        response = self.client.post(
            reverse("recipes:createrecipe"),
            {
                "name": "Gif Upload Recipe",
                "description": "Valid description",
                "cuisine": "other",
                "difficulty": "easy",
                "cooking_time": 15,
                "ingredients": "Water\nVegetables",
                "instructions": "Boil\nServe",
                "image": gif_file,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recipes.objects.filter(name="Gif Upload Recipe").exists())
        self.assertContains(response, "Image must be a JPG, PNG, or WEBP file.")


# Tests for saving recipes and viewing the saved recipes page.
class SavedRecipeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="saveduser", password="StrongPass123!")
        self.author = User.objects.create_user(username="recipeauthor", password="StrongPass123!")
        self.recipe = Recipes.objects.create(
            author=self.author,
            name="Garlic Bread",
            description="Buttery garlic bread",
            cuisine="other",
            difficulty="easy",
            cooking_time=10,
            ingredients="Bread\nButter\nGarlic",
            instructions="Mix\nSpread\nBake",
        )

    def test_logged_out_user_is_redirected_when_toggling_saved_recipe(self):
        response = self.client.post(reverse("recipes:toggle_save_recipe", args=[self.recipe.id]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("recipes:login"), response.url)
        self.assertEqual(SavedRecipe.objects.count(), 0)

    def test_logged_in_user_can_save_recipe(self):
        self.client.login(username="saveduser", password="StrongPass123!")

        response = self.client.post(reverse("recipes:toggle_save_recipe", args=[self.recipe.id]))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(SavedRecipe.objects.filter(user=self.user, recipe=self.recipe).exists())

    def test_second_toggle_removes_saved_recipe(self):
        self.client.login(username="saveduser", password="StrongPass123!")

        self.client.post(reverse("recipes:toggle_save_recipe", args=[self.recipe.id]))
        self.client.post(reverse("recipes:toggle_save_recipe", args=[self.recipe.id]))

        self.assertFalse(SavedRecipe.objects.filter(user=self.user, recipe=self.recipe).exists())

    def test_saved_page_shows_saved_recipe_for_logged_in_user(self):
        SavedRecipe.objects.create(user=self.user, recipe=self.recipe)
        self.client.login(username="saveduser", password="StrongPass123!")

        response = self.client.get(reverse("recipes:saved"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "viewcategory.html")
        self.assertContains(response, "Garlic Bread")


# Tests for posting and updating ratings and review comments.
class ReviewCommentTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="reviewauthor", password="StrongPass123!")
        self.user = User.objects.create_user(username="reviewuser", password="StrongPass123!")
        self.recipe = Recipes.objects.create(
            author=self.author,
            name="Tomato Pasta",
            description="Simple tomato pasta",
            cuisine="italian",
            difficulty="easy",
            cooking_time=20,
            ingredients="Pasta\nTomato sauce",
            instructions="Boil pasta\nAdd sauce",
        )

    def test_logged_out_user_is_redirected_when_posting_review(self):
        response = self.client.post(
            reverse("recipes:recipe_detail", args=[self.recipe.id]),
            {
                "value": 5,
                "comment": "Great recipe!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("recipes:login"))
        self.assertEqual(Rating.objects.count(), 0)

    def test_logged_in_user_can_post_review_and_comment(self):
        self.client.login(username="reviewuser", password="StrongPass123!")

        response = self.client.post(
            reverse("recipes:recipe_detail", args=[self.recipe.id]),
            {
                "value": 4,
                "comment": "Really tasty and easy to follow.",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("recipes:recipe_detail", args=[self.recipe.id]))
        rating = Rating.objects.get(recipe=self.recipe, user=self.user)
        self.assertEqual(rating.value, 4)
        self.assertEqual(rating.comment, "Really tasty and easy to follow.")

    def test_second_review_submission_updates_existing_rating(self):
        Rating.objects.create(recipe=self.recipe, user=self.user, value=3, comment="It was okay.")
        self.client.login(username="reviewuser", password="StrongPass123!")

        response = self.client.post(
            reverse("recipes:recipe_detail", args=[self.recipe.id]),
            {
                "value": 5,
                "comment": "Actually, this was excellent.",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Rating.objects.filter(recipe=self.recipe, user=self.user).count(), 1)
        rating = Rating.objects.get(recipe=self.recipe, user=self.user)
        self.assertEqual(rating.value, 5)
        self.assertEqual(rating.comment, "Actually, this was excellent.")


# Tests for review comment validation.
class ReviewValidationTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="reviewlimitauthor", password="StrongPass123!")
        self.user = User.objects.create_user(username="reviewlimituser", password="StrongPass123!")
        self.recipe = Recipes.objects.create(
            author=self.author,
            name="Validation Pasta",
            description="Simple pasta",
            cuisine="italian",
            difficulty="easy",
            cooking_time=20,
            ingredients="Pasta\nSauce",
            instructions="Boil\nServe",
        )
        self.client.login(username="reviewlimituser", password="StrongPass123!")

    def test_review_comment_cannot_be_longer_than_500_characters(self):
        response = self.client.post(
            reverse("recipes:recipe_detail", args=[self.recipe.id]),
            {
                "value": 5,
                "comment": "a" * 501,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rating.objects.count(), 0)
        self.assertContains(response, "Review comment cannot be longer than 500 characters.")


# Tests for homepage stats and recent uploads for logged-in users.
class HomepageContextTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="homepageuser", password="StrongPass123!")
        self.other_user = User.objects.create_user(username="otherhomepageuser", password="StrongPass123!")

        self.recipe1 = Recipes.objects.create(
            author=self.user,
            name="Recipe One",
            description="First recipe",
            cuisine="other",
            difficulty="easy",
            cooking_time=10,
            ingredients="A\nB",
            instructions="Step 1\nStep 2",
        )
        self.recipe2 = Recipes.objects.create(
            author=self.user,
            name="Recipe Two",
            description="Second recipe",
            cuisine="other",
            difficulty="easy",
            cooking_time=15,
            ingredients="A\nB",
            instructions="Step 1\nStep 2",
        )
        self.recipe3 = Recipes.objects.create(
            author=self.user,
            name="Recipe Three",
            description="Third recipe",
            cuisine="other",
            difficulty="easy",
            cooking_time=20,
            ingredients="A\nB",
            instructions="Step 1\nStep 2",
        )
        self.recipe4 = Recipes.objects.create(
            author=self.user,
            name="Recipe Four",
            description="Fourth recipe",
            cuisine="other",
            difficulty="easy",
            cooking_time=25,
            ingredients="A\nB",
            instructions="Step 1\nStep 2",
        )

        Rating.objects.create(recipe=self.recipe1, user=self.other_user, value=4, comment="Nice")
        Rating.objects.create(recipe=self.recipe2, user=self.other_user, value=5, comment="Great")
        Rating.objects.create(recipe=self.recipe4, user=self.user, value=5, comment="My own rating")

    def test_homepage_includes_logged_in_user_stats_and_recent_uploads(self):
        self.client.login(username="homepageuser", password="StrongPass123!")

        response = self.client.get(reverse("recipes:homepage"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("recent_uploads", response.context)
        self.assertIn("total_ratings_received", response.context)
        self.assertIn("total_ratings_given", response.context)
        self.assertIn("total_recipes_uploaded", response.context)
        self.assertEqual(response.context["total_ratings_received"], 3)
        self.assertEqual(response.context["total_ratings_given"], 1)
        self.assertEqual(response.context["total_recipes_uploaded"], 4)
        recent_upload_names = [recipe.name for recipe in response.context["recent_uploads"]]
        self.assertEqual(recent_upload_names, ["Recipe Four", "Recipe Three", "Recipe Two"])


# Tests for homepage top-rated ordering and search behaviour.
class HomepageTopRatedTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="topratedauthor", password="StrongPass123!")
        self.rater1 = User.objects.create_user(username="rater1", password="StrongPass123!")
        self.rater2 = User.objects.create_user(username="rater2", password="StrongPass123!")
        self.rater3 = User.objects.create_user(username="rater3", password="StrongPass123!")

        self.recipe1 = Recipes.objects.create(
            author=self.author,
            name="Alpha Curry",
            description="Recipe one",
            cuisine="indian",
            difficulty="easy",
            cooking_time=20,
            ingredients="A\nB",
            instructions="Step 1\nStep 2",
        )
        self.recipe2 = Recipes.objects.create(
            author=self.author,
            name="Beta Pasta",
            description="Recipe two",
            cuisine="italian",
            difficulty="easy",
            cooking_time=25,
            ingredients="A\nB",
            instructions="Step 1\nStep 2",
        )
        self.recipe3 = Recipes.objects.create(
            author=self.author,
            name="Gamma Burger",
            description="Recipe three",
            cuisine="other",
            difficulty="easy",
            cooking_time=15,
            ingredients="A\nB",
            instructions="Step 1\nStep 2",
        )

        Rating.objects.create(recipe=self.recipe1, user=self.rater1, value=5, comment="Great")
        Rating.objects.create(recipe=self.recipe1, user=self.rater2, value=5, comment="Great")
        Rating.objects.create(recipe=self.recipe2, user=self.rater1, value=4, comment="Good")
        Rating.objects.create(recipe=self.recipe3, user=self.rater1, value=3, comment="Okay")

    def test_homepage_top_rated_recipes_are_ordered_by_rating_then_count(self):
        response = self.client.get(reverse("recipes:homepage"))

        self.assertEqual(response.status_code, 200)
        top_rated_names = [recipe.name for recipe in response.context["top_rated_recipes"]]
        self.assertEqual(top_rated_names[:3], ["Alpha Curry", "Beta Pasta", "Gamma Burger"])

    def test_homepage_search_filters_top_rated_recipes_queryset(self):
        response = self.client.get(reverse("recipes:homepage"), {"q": "burger"})

        self.assertEqual(response.status_code, 200)
        top_rated_names = [recipe.name for recipe in response.context["top_rated_recipes"]]
        self.assertEqual(top_rated_names, ["Gamma Burger"])


# Tests for invalid recipe detail URLs and invalid rating values.
class RecipeDetailValidationTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="detailauthor", password="StrongPass123!")
        self.user = User.objects.create_user(username="detailuser", password="StrongPass123!")
        self.recipe = Recipes.objects.create(
            author=self.author,
            name="Detail Test Recipe",
            description="Recipe for detail tests",
            cuisine="other",
            difficulty="easy",
            cooking_time=15,
            ingredients="A\nB",
            instructions="Step 1\nStep 2",
        )

    def test_recipe_detail_with_invalid_id_returns_404(self):
        response = self.client.get(reverse("recipes:recipe_detail", args=[999999]))

        self.assertEqual(response.status_code, 404)

    def test_invalid_rating_value_is_rejected(self):
        self.client.login(username="detailuser", password="StrongPass123!")

        response = self.client.post(
            reverse("recipes:recipe_detail", args=[self.recipe.id]),
            {
                "value": 6,
                "comment": "Invalid rating value",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rating.objects.count(), 0)


# Test that recipe instructions are shown as separate steps.
class RecipeDetailRenderingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="renderuser", password="StrongPass123!")
        self.recipe = Recipes.objects.create(
            author=self.user,
            name="Layered Lasagna",
            description="A layered pasta bake",
            cuisine="italian",
            difficulty="medium",
            cooking_time=60,
            ingredients="Pasta\nCheese\nSauce",
            instructions="Prepare the sauce\nLayer the pasta\nBake until golden",
        )

    def test_recipe_detail_renders_multiline_instructions_as_separate_steps(self):
        response = self.client.get(reverse("recipes:recipe_detail", args=[self.recipe.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<li>Prepare the sauce</li>", html=True)
        self.assertContains(response, "<li>Layer the pasta</li>", html=True)
        self.assertContains(response, "<li>Bake until golden</li>", html=True)


# Test that recipe creation can save an uploaded image correctly.
@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class RecipeImageUploadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="imageuser", password="StrongPass123!")
        self.client.login(username="imageuser", password="StrongPass123!")

    def tearDown(self):
        from django.conf import settings
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_logged_in_user_can_create_recipe_with_image(self):
        image_buffer = io.BytesIO()
        image = Image.new("RGB", (10, 10), "white")
        image.save(image_buffer, format="JPEG")
        image_buffer.seek(0)

        image_file = SimpleUploadedFile(
            "test_recipe.jpg",
            image_buffer.getvalue(),
            content_type="image/jpeg",
        )

        response = self.client.post(
            reverse("recipes:createrecipe"),
            {
                "name": "Image Soup",
                "description": "Recipe with image",
                "cuisine": "other",
                "difficulty": "easy",
                "cooking_time": 10,
                "ingredients": "Water\nVegetables",
                "instructions": "Boil\nServe",
                "image": image_file,
            },
        )

        self.assertEqual(response.status_code, 302)
        recipe = Recipes.objects.get(name="Image Soup")
        self.assertTrue(bool(recipe.image))
        self.assertIn("test_recipe", recipe.image.name)

    def test_logged_in_user_cannot_create_recipe_with_image_over_5mb(self):
        image_buffer = io.BytesIO()
        large_image = Image.frombytes("RGB", (2200, 2200), os.urandom(2200 * 2200 * 3))
        large_image.save(image_buffer, format="PNG")
        image_buffer.seek(0)

        oversized_file = SimpleUploadedFile(
            "large_test.png",
            image_buffer.getvalue(),
            content_type="image/png",
        )

        self.assertGreater(len(oversized_file.read()), 5 * 1024 * 1024)
        oversized_file.seek(0)

        response = self.client.post(
            reverse("recipes:createrecipe"),
            {
                "name": "Huge Image Soup",
                "description": "Recipe with huge image",
                "cuisine": "other",
                "difficulty": "easy",
                "cooking_time": 10,
                "ingredients": "Water\nVegetables",
                "instructions": "Boil\nServe",
                "image": oversized_file,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recipes.objects.filter(name="Huge Image Soup").exists())
        self.assertContains(response, "Image size cannot be larger than 5MB.")
