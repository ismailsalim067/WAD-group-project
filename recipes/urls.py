from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path("", views.redirect_to_homepage, name="home"),
    path("homepage/", views.home, name="homepage"),
    path("createrecipe/", views.create_recipe, name="createrecipe")
    
]