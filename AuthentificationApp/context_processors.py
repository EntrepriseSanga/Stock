from .models import Produit
from django.db.models import F

def produits_critiques_count(request):
    nombre_produits_critiques = Produit.objects.filter(quantite_stock__lte=F('seuil_critique')).count()
    return {'nombre_produits_critiques': nombre_produits_critiques}
