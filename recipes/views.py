from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Recipe
from django.template.loader import render_to_string
from django.http import JsonResponse

# Create your views here.
def recipes(request):
    if not request.user.is_authenticated:
        recipes = Recipe.objects.all().select_related('user')
        return render(request, 'recipes/home.html', {'recipes': recipes})

    # fetches recipes of other users and also fetches user data too with just one query
    recipes = Recipe.objects.exclude(user = request.user).select_related('user')
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


@login_required(login_url='login')
def toggle_like(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if recipe.likes.filter(id=request.user.id).exists():
        recipe.likes.remove(request.user)
        liked = False
    else:
        recipe.likes.add(request.user)
        liked = True
        
    return JsonResponse({
        'liked': liked,
        'total_likes': recipe.likes.count()
    })


@login_required(login_url='login')
def toggle_bookmark(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if recipe.bookmarks.filter(id=request.user.id).exists():
        recipe.bookmarks.remove(request.user)
        bookmarked = False
    else:
        recipe.bookmarks.add(request.user)
        bookmarked = True
    
    return JsonResponse({
        'bookmarked': bookmarked,
    })