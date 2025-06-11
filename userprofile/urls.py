from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('profile/<int:id>', views.public_profile, name='public_profile'),
]
