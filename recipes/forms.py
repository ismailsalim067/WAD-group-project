from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from recipes.models import Recipes
from .models import Rating


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class RecipeForm(forms.ModelForm):
    cooking_time = forms.IntegerField(
        min_value=1,
        max_value=1440,
        error_messages={
            'min_value': 'Cooking time must be at least 1 minute.',
            'max_value': 'Cooking time cannot exceed 1440 minutes.',
            'required': 'Cooking time is required.',
        }
    )
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

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError('Recipe name cannot be blank.')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if not description:
            raise ValidationError('Description cannot be blank.')
        return description

    def clean_ingredients(self):
        ingredients = self.cleaned_data.get('ingredients', '').strip()
        if not ingredients:
            raise ValidationError('Ingredients cannot be blank.')
        return ingredients

    def clean_instructions(self):
        instructions = self.cleaned_data.get('instructions', '').strip()
        if not instructions:
            raise ValidationError('Instructions cannot be blank.')
        return instructions

    def clean_cooking_time(self):
        cooking_time = self.cleaned_data.get('cooking_time')
        if cooking_time is not None:
            if cooking_time < 1:
                raise ValidationError('Cooking time must be at least 1 minute.')
            if cooking_time > 1440:
                raise ValidationError('Cooking time cannot exceed 1440 minutes.')
        return cooking_time


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