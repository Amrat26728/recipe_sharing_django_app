from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipes, name='recipes'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('recipe_detail/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('toggle_like/<int:recipe_id>/', views.toggle_like, name='toggle_like'),
    path('toggle_bookmark/<int:recipe_id>/', views.toggle_bookmark, name='toggle_bookmark'),
]
