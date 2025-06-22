from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe, Comment
from django.http import JsonResponse, HttpResponse
from django.core import exceptions
from django.contrib import messages

# Create your views here.
def recipes(request):
    if not request.user.is_authenticated:
        recipes = Recipe.objects.select_related('user')
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
        image = request.FILES.get('recipe_image')
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
            image=image,
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
    try:
        recipe = Recipe.objects.get(id=id)
        comments = Comment.objects.filter(recipe=recipe).prefetch_related('user')

        return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'user': recipe.user.full_name, 'comments': comments})
    except Exception as e:
       return HttpResponse('Recipe id={} does not exist.'.format(id))


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

@login_required(login_url='login')
def delete_recipe(request, recipe_id):
    try:
        Recipe.objects.filter(
            id=recipe_id,
            user=request.user
        ).delete()
        messages.success(request, "recipe with id={} is deleted.".format(recipe_id))
        return redirect('profile')
    except exceptions as e:
        messages.error(request, str(e))
        return redirect('profile')

@login_required(login_url='login')
def add_comment(request, recipe_id):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        if comment:
            recipe = Recipe.objects.get(id=recipe_id)
            Comment.objects.create(
                recipe=recipe,
                user=request.user,
                comment=comment
            )
            messages.success(request, "Comment added.")
            return redirect('recipe_detail', id=recipe_id)
        else:
            messages.error(request, "Enter comment first")
            return redirect('recipe_detail', id=recipe_id)
    
    return redirect('recipe_detail', id=recipe_id)