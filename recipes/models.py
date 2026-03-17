from django.db import models
from django.contrib.auth.models import User

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