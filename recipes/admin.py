from django.contrib import admin
from .models import Rating, Recipes, SavedRecipe

admin.site.register(Recipes)
admin.site.register(Rating)
admin.site.register(SavedRecipe)
