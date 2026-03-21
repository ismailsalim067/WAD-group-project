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
    recipes = Recipes.objects.all()

    if query:
        recipes = recipes.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(ingredients__icontains=query)
            | Q(cuisine__icontains=query)
        )

    return render(request, "homepage.html", {
        "recipes": recipes,
        "query": query,
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
