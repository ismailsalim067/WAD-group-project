from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from recipes.models import Recipes


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipes
        fields = [
            'name',
            'description',
            'cuisine',
            'difficulty',
            'cooking_time',
            'ingredients',
            'instructions',
        ]