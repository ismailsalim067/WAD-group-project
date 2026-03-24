from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from recipes.models import Recipes
from .models import Rating


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


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value', 'comment']
        widgets = {
            'value': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'rows': 2,              
                'class': 'form-control',
                'style': 'resize: none;'  
            })
        }