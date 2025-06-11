
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('profile/', include('userprofile.urls')),
    path('', include('recipes.urls')),
]
