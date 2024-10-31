from django.contrib import admin
from django.urls import path, include  # Import de `include` pour inclure les URLs des apps

urlpatterns = [
    path('admin/', admin.site.urls),  # URL pour l'administration Django
    path('', include('AuthentificationApp.urls')),  # Inclusion des URLs de votre app
]
