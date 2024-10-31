from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur,CategorieProduit


class RegistrationForm(UserCreationForm):
    telephone = forms.CharField(max_length=15, required=True, help_text="Numéro de téléphone")

    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'telephone', 'password1', 'password2']

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email or Username", max_length=254)


class UtilisateurForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'telephone', 'email', 'role', 'password1', 'password2']


from django import forms
from .models import CategorieProduit

class CategorieForm(forms.ModelForm):
    class Meta:
        model = CategorieProduit
        fields = ['nom', 'description']


from django import forms
from .models import Produit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix_achat', 'prix_unitaire', 'quantite_stock', 'seuil_critique', 'categorie']



from django import forms
from .models import Vente, Client, VenteProduit

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'telephone','CNIB']

class VenteProduitForm(forms.ModelForm):
    class Meta:
        model = VenteProduit
        fields = ['quantite_vendue', 'rabais_produit']

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['type_paiement']
