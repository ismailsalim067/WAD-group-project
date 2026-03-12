from django.db import models

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
    ('hard', 'hard'),
]

class Recipes(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    cuisine = models.CharField(max_length=50, choices=CUISINE_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    cooking_time = models.PositiveIntegerField()
    ingredients = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.name