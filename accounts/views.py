from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import User

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('recipes')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if not user:
            messages.error(request, 'Invalid email or password')
            return render(request, 'accounts/login.html')
        else:
            login(request, user)
            return redirect('recipes')

    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        full_name = request.POST['fullname']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if not email:
            messages.error(request, 'Email is required')
            return render(request, 'acconts/signup.html')
        
        if not full_name:
            messages.error(request, 'Full name is required')
            return render(request, 'acconts/signup.html')
            
        if not password:
            messages.error(request, 'Password is required')
            return render(request, 'acconts/signup.html')
            
        if not confirm_password:
            messages.error(request, 'Confirm password is required')
            return render(request, 'acconts/signup.html')
            
        
        user = User.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            bio=""
        )
        login(request, user)
        return redirect('recipes')

    return render(request, 'accounts/signup.html')

def logout_view(request):
    logout(request)
    return redirect('recipes')