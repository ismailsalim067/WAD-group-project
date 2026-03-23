from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path("", views.redirect_to_homepage, name="home"),
    path("homepage/", views.home, name="homepage"),
    path("viewcategory/<str:category>/", views.view_category, name="view_category"),
    path("createrecipe/", views.create_recipe, name="createrecipe"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("myrecipes/", views.my_recipes, name="myrecipes"),
    path('myrecipes/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path("saved/", views.saved_view, name="saved"),

]