from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe
from accounts.models import User

# Create your views here.
def recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/home.html', {'recipes': recipes})

@login_required(login_url='login')
def add_recipe(request):

    if request.method == 'POST':
        # Get basic recipe data
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        prep_time = request.POST.get('prep_time')
        cook_time = request.POST.get('cook_time')
        servings = request.POST.get('servings')
        difficulty = request.POST.get('difficulty')
        chef_note = request.POST.get('chef_note')

        # Process ingredients - using getlist() to get all values
        ingredients = request.POST.getlist('ingredients[]')
        instructions = request.POST.getlist('instructions[]')

        ingredients = [item.strip() for item in ingredients if item.strip()]
        instructions = [item.strip() for item in instructions if item.strip()]

        # Create the recipe
        recipe = Recipe.objects.create(
            user=request.user,
            title=title,
            description=description,
            prep_time=prep_time,
            cook_time=cook_time,
            servings=servings,
            category=category,
            difficulty=difficulty,
            chef_note=chef_note,
            ingredients=ingredients,
            instructions=instructions
        )
        
        return redirect('recipe_detail', id=recipe.id)

    return render(request, 'recipes/add_recipe.html')

def recipe_detail(request, id):

    recipe = Recipe.objects.get(id=id)

    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'instruction_counter': 0, 'user': recipe.user.full_name})