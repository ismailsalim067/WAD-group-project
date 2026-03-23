from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import RecipeForm, SignUpForm
from .models import Recipes


# Create your views here.

def home(request):
    query = request.GET.get("q", "").strip()
    difficulty = request.GET.get("difficulty", "").strip().lower()
    recipes = Recipes.objects.all()

    if query:
        recipes = recipes.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(ingredients__icontains=query)
            | Q(cuisine__icontains=query)
        )

    if difficulty in {"easy", "medium", "hard"}:
        recipes = recipes.filter(difficulty=difficulty)

    return render(request, "homepage.html", {
        "recipes": recipes,
        "query": query,
        "selected_difficulty": difficulty,
    })


def redirect_to_homepage(request):
    return redirect("/homepage/")


@login_required
@csrf_exempt
def create_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            return redirect('recipes:recipe_detail', id=recipe.id)
        
    else:        
        form = RecipeForm()

    return render(request, "createrecipe.html", {'form':form})


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

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipes, id=id)

    return render(request, "recipedetail.html", {'recipe':recipe})


def logout_view(request):
    auth_logout(request)
    return redirect("/homepage/")

def saved_view(request):
    return HttpResponse("Starter save page view")

def get_hint(request):
    recipes = [
        "Apple Crumble",
        "Avocado Toast",
        "Banana Bread",
        "Beef Stew",
        "Cinnamon Buns",
        "Chicken Ceasar Salad",
        "Doughnuts",
        "Dumplings",
        "Eclairs",
        "Egg Benedict",
        "French Toast",
        "Fried Rice",
        "Gingerbread Cookies",
        "Garlic Bread",
        "Hot Cross Buns",
        "Hummus",
        "Ice Cream",
        "Italian Meatballs",
        "Jelly",
        "Jerk Chicken",
        "Key Lime Pie",
        "Kebab",
        "Lemon Meringue Pie",
        "Lasagna",
        "Muffins",
        "Macaroni and Cheese",
        "Nougat",
        "Nachos",
        "Overnight Oats",
        "Omelette",
        "Pancakes",
        "Pizza",
        "Quiche",
        "Quesadilla",
        "Red Velvet Cake",
        "Ratatouille",
        "Scones",
        "Spaghetti Bolognese",
        "Tiramisu",
        "Tacos",
        "Upside Down Cake",
        "Udon Noodles",
        "Victoria Sponge Cake",
        "Vegetable Stir Fry",
        "Waffles",
        "Welsh Rarebit",
        "Yorkshire Pudding",
    ]
    q = request.GET.get("q", "").lower()
    suggestions = [r for r in recipes if r.lower().startswith(q)]
    return HttpResponse(", ".join(suggestions) if suggestions else "No suggestions")

