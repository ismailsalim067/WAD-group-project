from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

CUISINE_CHOICES = [
    ('italian', 'Italian'),
    ('indian', 'Indian'),
    ('mexican', 'Mexican'),
    ('chinese', 'Chinese'),
    ('other', 'Other'),
]

DIFFICULTY_CHOICES = [
    ('easy' , 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
]

RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

class Recipes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=128)
    description = models.TextField()
    cuisine = models.CharField(max_length=50, choices=CUISINE_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    cooking_time = models.PositiveIntegerField()
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    value = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'user'], name='unique_user_recipe_rating')
        ]

    def __str__(self):
        return f"{self.user.username} rated {self.recipe.name}: {self.value}"
    

class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_recipes')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='saved')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'], name='saved_recipe')
        ]

    def __str__(self):
        return f"{self.user.username} saved {self.recipe.name}"