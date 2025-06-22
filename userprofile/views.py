from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from accounts.models import User
from django.contrib import messages
from django.urls import reverse

# Create your views here.
@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        try:
            full_name = request.POST.get('fullName')
            bio = request.POST.get('bio')
            location = request.POST.get('location')
            profile_image = request.FILES.get('profile_image')
            user = User.objects.get(id=request.user.id)
            
            user.full_name = full_name
            user.bio = bio
            user.location = location
            if profile_image:
                user.profile_image = profile_image
            user.save()
            
            messages.success(request, 'Updated successfully!')
            return redirect('profile')
        except Exception as e:
            messages.error(request, 'Something went wrong!')
            return redirect('profile')
        
    recipes = Recipe.objects.filter(user=request.user).prefetch_related(
        'likes',
        'bookmarks'
    )
    liked_recipes = Recipe.objects.filter(likes=request.user)
    bookmarked_recipes = Recipe.objects.filter(bookmarks=request.user)

    return render(request, 'userprofile/profile.html', {'user': request.user, 'recipes': recipes, 'no_of_recipes': recipes.count(), 'liked_recipes': liked_recipes, 'bookmarked_recipes': bookmarked_recipes})


def public_profile(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = User.objects.get(id=id)
            if request.user.following.filter(id=user.id).exists():
                request.user.following.remove(user)
                is_following = False
            else:
                request.user.following.add(user)
                is_following = True
            return redirect('public_profile', id=id)
            
        else:
            return redirect('login')


    user = User.objects.get(id=id)
    recipes = Recipe.objects.filter(user = user)
    no_of_recipes = recipes.count()
    is_following = False
    if request.user.following.filter(id=user.id).exists():
        is_following = True
    return render(request, 'userprofile/public_profile.html', {'user': user, 'recipes': recipes, 'no_of_recipes': no_of_recipes, 'is_following': is_following})
