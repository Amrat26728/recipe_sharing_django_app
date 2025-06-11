from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from accounts.models import User

# Create your views here.
@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        return redirect('profile')
    
    recipes = Recipe.objects.filter(user = request.user)
    return render(request, 'userprofile/profile.html', {'user': request.user, 'recipes': recipes, 'no_of_recipes': recipes.count()})


def public_profile(request, id):
    # fetches only one user
    user = User.objects.get(id=id)
    # countes the recipes of user, does not fetches recipes data
    no_of_recipes = Recipe.objects.filter(user = user).count()
    return render(request, 'userprofile/public_profile.html', {'user': user, 'no_of_recipes': no_of_recipes})