from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import RecipeForm, SignUpForm, RatingForm
from .models import Recipes, Rating, SavedRecipe
from django.db.models import Avg


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
    
    if request.user.is_authenticated:
        return render(request, "homepage.html", {
        "recipes": recipes,
        "query": query,
        "selected_difficulty": "",
    })
    else:
        return render(request, "logged_out_homepage.html")
    

    


def view_category(request, category):
    query = request.GET.get("q", "").strip()
    category = category.strip().lower()
    recipes = Recipes.objects.all()

    if query:
        recipes = recipes.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(ingredients__icontains=query)
            | Q(cuisine__icontains=query)
        )

    if category in {"easy", "medium", "hard"}:
        recipes = recipes.filter(difficulty=category)

    return render(request, "viewcategory.html", {
        "recipes": recipes,
        "query": query,
        "selected_difficulty": category,
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

    ratings = Rating.objects.filter(recipe=recipe).select_related('user')
    existing_rating = Rating.objects.filter(recipe=recipe, user=request.user).first()

    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedRecipe.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists()

    if request.method == "POST":
        
        form = RatingForm(request.POST, instance=existing_rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.recipe = recipe
            rating.user = request.user
            rating.save()

            return redirect('recipes:recipe_detail', id=recipe.id)
        
    else: 
        form = RatingForm(instance=existing_rating)

    average_rating = ratings.aggregate(avg=Avg('value'))['avg']
    average_rating = round(average_rating, 1) if average_rating else 0

    context = {
        'recipe': recipe,
        'ratings': ratings,
        'form': form,
        'existing_rating': existing_rating,
        'average_rating': average_rating,
        'rating_count': ratings.count(),
        'is_saved' : is_saved,
    }

    return render(request, "recipedetail.html", context)


def logout_view(request):
    auth_logout(request)
    return redirect("/homepage/")

@login_required
def toggle_save_recipe(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipes, id=recipe_id)
        saved_qs = SavedRecipe.objects.filter(user=request.user, recipe=recipe)

        if saved_qs.exists():
            saved_qs.delete()
            saved = False
        else:
            SavedRecipe.objects.create(user=request.user, recipe=recipe)
            saved = True

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'saved':saved})
        
    return redirect(request.META.get('HTTP_REFERER', 'recipes:homepage'))

@login_required
def saved_view(request):
    saved = SavedRecipe.objects.filter(user=request.user).select_related('recipe')
    recipes = [s.recipe for s in saved]

    recipe_list = "".join([f"<li>{r.name}</li>" for r in recipes])
    return HttpResponse(f"<ul>{recipe_list}</ul>")

