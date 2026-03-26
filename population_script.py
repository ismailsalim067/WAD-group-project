import os
import random
from django.core.files import File

# Set up Django so this script can use the project models.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipeasy.settings")

import django

django.setup()

from django.contrib.auth.models import User
from recipes.models import Recipes, Rating, SavedRecipe


def populate():
    print("Starting RecipEasy population script")

    # Demo users for testing login, ratings, and saved recipes.
    demo_users = [
        {"username": "ismail", "password": "test12345"},
        {"username": "adam", "password": "test12345"},
        {"username": "zoe", "password": "test12345"},
        {"username": "molly", "password": "test12345"},
        {"username": "lewis", "password": "test12345"},
    ]

    created_users = []

    # Create the demo users if they do not already exist.
    for user_data in demo_users:
        user, created = User.objects.get_or_create(username=user_data["username"])
        if created:
            user.set_password(user_data["password"])
            user.save()
            print(f"Created user: {user.username}")
        else:
            print(f"User already exists: {user.username}")
        created_users.append(user)

    # Sample recipe data used to populate the site.
    recipe_data = [
        {
            "author": "ismail",
            "name": "Chicken Curry",
            "description": "A warming curry with chicken and spices.",
            "cuisine": "indian",
            "difficulty": "medium",
            "cooking_time": 45,
            "ingredients": "Chicken\nOnion\nGarlic\nCurry paste\nCoconut milk",
            "instructions": "Cook the onion and garlic.\nAdd the chicken and curry paste.\nStir in the coconut milk.\nSimmer until the chicken is cooked through.",
            "image": "chicken_curry.jpg",
        },
        {
            "author": "adam",
            "name": "Steak",
            "description": "Pan-seared steak cooked until juicy and tender.",
            "cuisine": "other",
            "difficulty": "medium",
            "cooking_time": 20,
            "ingredients": "Steak\nButter\nGarlic\nSalt\nPepper",
            "instructions": "Season the steak.\nSear it in a hot pan with butter and garlic.\nRest before serving.",
            "image": "steak.jpg",
        },
        {
            "author": "zoe",
            "name": "Spaghetti Bolognese",
            "description": "A classic Italian pasta dish with rich meat sauce.",
            "cuisine": "italian",
            "difficulty": "easy",
            "cooking_time": 40,
            "ingredients": "Spaghetti\nMinced beef\nOnion\nGarlic\nTomato sauce",
            "instructions": "Boil the pasta.\nCook the beef with onion and garlic.\nAdd the tomato sauce.\nCombine and serve.",
        },
        {
            "author": "molly",
            "name": "Pizza",
            "description": "Homemade pizza with tomato sauce and melted cheese.",
            "cuisine": "italian",
            "difficulty": "easy",
            "cooking_time": 25,
            "ingredients": "Pizza dough\nTomato sauce\nMozzarella\nBasil",
            "instructions": "Spread the sauce on the dough.\nAdd the mozzarella and basil.\nBake until golden.",
        },
        {
            "author": "lewis",
            "name": "Burgers",
            "description": "Juicy homemade beef burgers served in toasted buns.",
            "cuisine": "other",
            "difficulty": "easy",
            "cooking_time": 20,
            "ingredients": "Minced beef\nBurger buns\nLettuce\nCheese",
            "instructions": "Shape the beef into patties.\nCook them in a pan.\nServe in buns with the toppings.",
        },
    ]

    created_recipes = []

    # Add images to seeded recipes when matching files are available locally.
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
            recipe.description = data["description"]
            recipe.cuisine = data["cuisine"]
            recipe.difficulty = data["difficulty"]
            recipe.cooking_time = data["cooking_time"]
            recipe.ingredients = data["ingredients"]
            recipe.instructions = data["instructions"]
            recipe.save()
            print(f"Updated recipe: {recipe.name}")

        image_name = data.get("image")
        if image_name:
            image_path = os.path.join("media", "recipe_images", image_name)
            if os.path.exists(image_path):
                with open(image_path, "rb") as image_file:
                    recipe.image.save(image_name, File(image_file), save=False)
                recipe.save()

        created_recipes.append(recipe)

    # Add a couple of ratings and comments to each recipe.
    for recipe in created_recipes:
        rating_users = random.sample(created_users, k=min(2, len(created_users)))
        for user in rating_users:
            sample_comments = [
                "Really easy to follow and tasted great.",
                "Loved this recipe and would make it again.",
                "Simple ingredients and very good flavour.",
                "Turned out well and was perfect for dinner.",
                "Quick to make and everyone enjoyed it.",
                "Clear steps and a solid result overall.",
            ]
            rating, created = Rating.objects.get_or_create(
                recipe=recipe,
                user=user,
                defaults={
                    "value": random.randint(3, 5),
                    "comment": random.choice(sample_comments),
                },
            )
            if created:
                print(f"Added rating for {recipe.name} by {user.username}")

    # Sample saved recipes so this feature can be tested straight away.
    saved_recipe_pairs = [
        ("ismail", "Pizza"),
        ("ismail", "Spaghetti Bolognese"),
        ("adam", "Chicken Curry"),
        ("zoe", "Steak"),
        ("molly", "Burgers"),
    ]

    # Link users to some saved recipes.
    for username, recipe_name in saved_recipe_pairs:
        user = User.objects.get(username=username)
        recipe = Recipes.objects.get(name=recipe_name)
        saved_recipe, created = SavedRecipe.objects.get_or_create(user=user, recipe=recipe)
        if created:
            print(f"Saved recipe: {recipe.name} for {user.username}")

    print("Population complete.")


# Run the script when this file is executed directly.
if __name__ == "__main__":
    populate()