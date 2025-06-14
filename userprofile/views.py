from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from accounts.models import User
from django.contrib import messages

# Create your views here.
@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        # user = User.objects.get(id=request.user.id)
        try:
            full_name = request.POST.get('fullName')
            bio = request.POST.get('bio')
            location = request.POST.get('location')
            User.objects.filter(id=request.user.id).update(
                full_name = full_name,
                bio = bio,
                location = location
            )
            
            messages.success(request, 'Updated successfully!')
            return redirect('profile')
        except Exception as e:
            messages.error(request, 'Something went wrong!')
            return redirect('profile')
        
    recipes = Recipe.objects.filter(user=request.user).prefetch_related(
        'likes',
        'bookmarks'
    ).select_related('user').all()
    liked_recipes = Recipe.objects.filter(likes=request.user)
    bookmarked_recipes = Recipe.objects.filter(bookmarks=request.user)

    return render(request, 'userprofile/profile.html', {'user': request.user, 'recipes': recipes, 'no_of_recipes': recipes.count(), 'liked_recipes': liked_recipes, 'bookmarked_recipes': bookmarked_recipes})


def public_profile(request, id):
    # fetches only one user
    user = User.objects.get(id=id)
    # countes the recipes of user, does not fetches recipes data
    recipes = Recipe.objects.filter(user = user)
    following_count = user.following.count()
    followers_count = user.followers.count()
    no_of_recipes = recipes.count()
    return render(request, 'userprofile/public_profile.html', {'user': user, 'recipes': recipes, 'no_of_recipes': no_of_recipes, 'following': following_count, 'followers': followers_count})
