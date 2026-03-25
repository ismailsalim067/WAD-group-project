import os
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipeasy.settings")

import django

django.setup()

from django.contrib.auth.models import User
from recipes.models import Recipes, Rating, SavedRecipe


def populate():
    print("Starting RecipEasy population script")

    demo_users = [
        {"username": "ismail", "password": "test12345"},
        {"username": "adam", "password": "test12345"},
        {"username": "zoe", "password": "test12345"},
        {"username": "molly", "password": "test12345"},
        {"username": "lewis", "password": "test12345"},
    ]

    created_users = []

    for user_data in demo_users:
        user, created = User.objects.get_or_create(username=user_data["username"])
        if created:
            user.set_password(user_data["password"])
            user.save()
            print(f"Created user: {user.username}")
        else:
            print(f"User already exists: {user.username}")
        created_users.append(user)

    recipe_data = [
        {
            "author": "ismail",
            "name": "Chicken Curry",
            "description": "A warming curry with chicken and spices.",
            "cuisine": "indian",
            "difficulty": "medium",
            "cooking_time": 45,
            "ingredients": "Chicken, onion, garlic, curry paste, coconut milk",
            "instructions": "Cook onion and garlic. Add chicken and curry paste. Stir in coconut milk and simmer.",
        },
        {
            "author": "adam",
            "name": "Steak",
            "description": "Pan-seared steak cooked until juicy and tender.",
            "cuisine": "other",
            "difficulty": "medium",
            "cooking_time": 20,
            "ingredients": "Steak, butter, garlic, salt, pepper",
            "instructions": "Season the steak. Sear in a hot pan with butter and garlic. Rest before serving.",
        },
        {
            "author": "zoe",
            "name": "Spaghetti Bolognese",
            "description": "A classic Italian pasta dish with rich meat sauce.",
            "cuisine": "italian",
            "difficulty": "easy",
            "cooking_time": 40,
            "ingredients": "Spaghetti, minced beef, onion, garlic, tomato sauce",
            "instructions": "Boil pasta. Cook beef with onion and garlic. Add tomato sauce. Combine and serve.",
        },
        {
            "author": "molly",
            "name": "Pizza",
            "description": "Homemade pizza with tomato sauce and melted cheese.",
            "cuisine": "italian",
            "difficulty": "easy",
            "cooking_time": 25,
            "ingredients": "Pizza dough, tomato sauce, mozzarella, basil",
            "instructions": "Spread sauce on the dough, add cheese, and bake until golden.",
        },
        {
            "author": "lewis",
            "name": "Burgers",
            "description": "Juicy homemade beef burgers served in toasted buns.",
            "cuisine": "other",
            "difficulty": "easy",
            "cooking_time": 20,
            "ingredients": "Minced beef, burger buns, lettuce, cheese",
            "instructions": "Shape the beef into patties, cook in a pan, and serve in buns with the toppings.",
        },
    ]

    created_recipes = []

    for data in recipe_data:
        author = User.objects.get(username=data["author"])

        recipe, created = Recipes.objects.get_or_create(
            name=data["name"],
            author=author,
            defaults={
                "description": data["description"],
                "cuisine": data["cuisine"],
                "difficulty": data["difficulty"],
                "cooking_time": data["cooking_time"],
                "ingredients": data["ingredients"],
                "instructions": data["instructions"],
            },
        )

        if created:
            print(f"Created recipe: {recipe.name}")
        else:
            print(f"Recipe already exists: {recipe.name}")

        created_recipes.append(recipe)

    for recipe in created_recipes:
        rating_users = random.sample(created_users, k=min(2, len(created_users)))
        for user in rating_users:
            rating, created = Rating.objects.get_or_create(
                recipe=recipe,
                user=user,
                defaults={"value": random.randint(3, 5)},
            )
            if created:
                print(f"Added rating for {recipe.name} by {user.username}")

    saved_recipe_pairs = [
        ("ismail", "Pizza"),
        ("ismail", "Spaghetti Bolognese"),
        ("adam", "Chicken Curry"),
        ("zoe", "Steak"),
        ("molly", "Burgers"),
    ]

    for username, recipe_name in saved_recipe_pairs:
        user = User.objects.get(username=username)
        recipe = Recipes.objects.get(name=recipe_name)
        saved_recipe, created = SavedRecipe.objects.get_or_create(user=user, recipe=recipe)
        if created:
            print(f"Saved recipe: {recipe.name} for {user.username}")

    print("Population complete.")


if __name__ == "__main__":
    populate()