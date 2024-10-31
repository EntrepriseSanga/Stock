from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db import models
from decimal import Decimal
import string
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save


# Table Utilisateur (Custom User)
class Utilisateur(AbstractUser):
    boutique = models.ForeignKey('Boutique', on_delete=models.CASCADE, null=True, blank=True)
    telephone = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('employe', 'Employé')])
    statut = models.CharField(max_length=10, choices=[('actif', 'Actif'), ('inactif', 'Inactif')])
    date_de_connexion = models.DateTimeField(null=True, blank=True)
    

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='utilisateur_groups',  # Ajouter un related_name unique
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='utilisateur_permissions',  # Ajouter un related_name unique
        blank=True
    )

# Table Boutique
class Boutique(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

# Table CategorieProduit
class CategorieProduit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nom

# Table Produit
class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_stock = models.PositiveIntegerField()
    seuil_critique = models.PositiveIntegerField()
    categorie = models.ForeignKey(CategorieProduit, on_delete=models.CASCADE)


    date_creation = models.DateField(default=timezone.now)

    def __str__(self):
        return self.nom


#vente table

class Vente(models.Model):
    date_vente = models.DateTimeField(auto_now_add=True)
    type_paiement = models.CharField(max_length=10, choices=[('cash', 'Cash'), ('credit', 'Crédit')], default='cash')
    total_rabais = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_encaisse = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, blank=True)
    nombre_vente_journee = models.IntegerField(default=0)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    etait_credits=models.BooleanField(default=False)

# Réinitialisation de `nombre_vente_journee` à 0 à minuit
@receiver(post_save, sender=Vente)
def reset_ventes_journee(sender, instance, **kwargs):
    current_time = timezone.now()
    if current_time.hour == 0 and current_time.minute == 0:
        Vente.objects.update(nombre_vente_journee=0)



# Table VenteProduit
class VenteProduit(models.Model):
    vente = models.ForeignKey('Vente', on_delete=models.CASCADE)
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    quantite_vendue = models.PositiveIntegerField()
    rabais_produit = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Rabais par produit
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

   
# Table Facture

class Facture(models.Model):
    vente = models.OneToOneField('Vente', on_delete=models.CASCADE)
    fichier_pdf = models.FileField(upload_to='factures/')
    numero = models.CharField(max_length=20, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = self.generer_numero()
        super().save(*args, **kwargs)

    def generer_numero(self):
        """
        Génère un numéro de facture alphanumérique unique.
        """
        # Exemple de génération : FCT-XXXX (où XXXX est un nombre aléatoire)
        prefix = "FCT-"
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"{prefix}{suffix}"

    def __str__(self):
        return f"Facture {self.numero} pour la vente {self.vente.id}"


# Table Client
class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=15)
    adresse = models.CharField(max_length=255)
    total_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_paiement = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    CNIB = models.CharField(max_length=10, null=True, blank=True,unique=True)

    def __str__(self):
        return self.nom

# Table Stock
class Stock(models.Model):
    date_entree = models.DateTimeField(auto_now_add=True)
    quantite = models.PositiveIntegerField()
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)

    def __str__(self):
        return f"Stock de {self.produit.nom}"

# Table Historique
class Historique(models.Model):
    type_action = models.CharField(max_length=20, choices=[('vente', 'Vente'), ('entree', 'Entrée produit'), ('modification', 'Modification stock')])
    date_action = models.DateTimeField(auto_now_add=True)
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
    boutique = models.ForeignKey(Boutique, on_delete=models.SET_NULL, null=True)
    details_action = models.TextField()

    def __str__(self):
        return f"Action {self.type_action} sur {self.produit}"

# Table Rapport
class Rapport(models.Model):
    date_rapport = models.DateTimeField(auto_now_add=True)
    type_rapport = models.CharField(max_length=20, choices=[('journalier', 'Journalier'), ('mensuel', 'Mensuel')])
    total_cash = models.DecimalField(max_digits=10, decimal_places=2)
    total_credit = models.DecimalField(max_digits=10, decimal_places=2)
    benefice_total = models.DecimalField(max_digits=10, decimal_places=2)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Rapport {self.type_rapport} - {self.date_rapport}"

# Table Notification
class Notification(models.Model):
    date_notification = models.DateTimeField(auto_now_add=True)
    type_notification = models.CharField(max_length=20, choices=[('connexion', 'Connexion'), ('sortie_produit', 'Sortie produit'), ('stock_critique', 'Stock critique')])
    message = models.TextField()
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Notification {self.type_notification}"

# Table Remboursement
class Remboursement(models.Model):
    date_remboursement = models.DateTimeField(auto_now_add=True)
    montant_rembourse = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return f"Remboursement {self.client.nom} - {self.montant_rembourse} €"

class Credits(models.Model):
        vente = models.ForeignKey(Vente, on_delete=models.CASCADE)
        date_paiement = models.DateTimeField()
        montant = models.DecimalField(max_digits=10, decimal_places=2)
        pdf=models.FileField(upload_to="factures/")

        # Ajoutez d'autres champs utiles comme un champ 'note' pour les informations supplémentaires

        def __str__(self):
            return f"Crédit payé pour la vente {self.vente.id} - {self.montant} f"
from django.db import models
from django.utils import timezone

class ProdVenduMois(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    mois = models.DateField()  # Date du mois (ex : 2024-10-01 pour le mois d'octobre)
    quantite_vendue = models.PositiveIntegerField(default=0)  # Quantité totale vendue durant le mois
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2,default=0)  # Prix unitaire du produit
    total_encaisse = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total encaissé pour ce produit durant le mois

    class Meta:
        unique_together = ('produit', 'mois')  # Ensure each product has only one entry per month

    def __str__(self):
        return f"Ventes de {self.produit.nom} pour le mois {self.mois.strftime('%B %Y')}"




# Signal to increment `quantite_vendue` in ProdVenduMois after a VenteProduit is saved

@receiver(post_save, sender=VenteProduit)
def increment_prod_vendu_mois(sender, instance, **kwargs):
    current_month = timezone.now().replace(day=1)  # Premier jour du mois actuel
    produit = instance.produit

    # Récupérer ou créer l'entrée pour le produit vendu ce mois-ci
    prod_vendu_mois, created = ProdVenduMois.objects.get_or_create(
        produit=produit,
        mois=current_month,
        defaults={'prix_unitaire': produit.prix_unitaire}  # Si l'entrée est créée, ajouter le prix unitaire
    )

    # Incrémenter la quantité vendue et mettre à jour le total encaissé
    prod_vendu_mois.quantite_vendue += instance.quantite_vendue
    prod_vendu_mois.total_encaisse += instance.quantite_vendue * produit.prix_unitaire  # Met à jour le total encaissé

    # Sauvegarder les changements
    prod_vendu_mois.save()


