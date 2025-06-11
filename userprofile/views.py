from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from accounts.models import User

# Create your views here.
@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        return redirect('profile')
    
    no_of_recipes = Recipe.objects.filter(user=request.user).count()
    return render(request, 'userprofile/profile.html', {'user': request.user, 'no_of_recipes': no_of_recipes})


def public_profile(request, id):
    user = User.objects.get(id=id)
    return render(request, 'userprofile/public_profile.html', {'user': user})