from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Recipes



# Create your views here.

def home(request):
    #return render(request)
    return HttpResponse("Recipes Home page")

def redirect_to_homepage(request):
    return redirect("homepage/")

def create_recipe(request):
    return HttpResponse("Create Recipe view")




def create_recipe(request):

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        cuisine = request.POST.get("cuisine")
        difficulty = request.POST.get("difficulty")
        cooking_time = request.POST.get("cooking_time")
        ingredients = request.POST.get("ingredients")
        instructions = request.POST.get("instructions")

        recipe = Recipes.objects.create(
            name=name,
            description=description,
            cuisine=cuisine,
            difficulty=difficulty,
            cooking_time=cooking_time,
            ingredients=ingredients,
            instructions=instructions
        )

        return HttpResponse(f"Recipe {recipe.name} created")
     
    return HttpResponse('Waiting for recipe submission')




