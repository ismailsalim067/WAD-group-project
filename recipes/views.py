from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import SignUpForm
from .models import Recipes


# Create your views here.

def home(request):
    return render(request, "homepage.html")


def redirect_to_homepage(request):
    return redirect("/homepage/")


@login_required
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
            author=request.user,
            name=name,
            description=description,
            cuisine=cuisine,
            difficulty=difficulty,
            cooking_time=cooking_time,
            ingredients=ingredients,
            instructions=instructions,
        )

        return HttpResponse(f"Recipe {recipe.name} created")

    return HttpResponse("Waiting for recipe submission")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("/homepage/")

        return render(request, "login.html", {"error": "Invalid username or password."})

    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("/homepage/")
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})


@login_required
def my_recipes(request):
    user_recipes = Recipes.objects.filter(author=request.user)
    return HttpResponse(f"You have {user_recipes.count()} recipe(s).")


def logout_view(request):
    auth_logout(request)
    return redirect("/homepage/")
