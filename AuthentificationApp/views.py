from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import LoginForm, RegistrationForm
from django.http import FileResponse
from django.shortcuts import render

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

from django.shortcuts import render, redirect
from .models import Utilisateur

def signup_view(request):
    if request.method == 'POST':
        # Récupérer les informations du formulaire
        username = request.POST.get('username')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        password = request.POST.get('password')

        # Créer l'utilisateur avec le rôle 'employé' par défaut
        if not Utilisateur.objects.filter(username=username).exists():
            utilisateur = Utilisateur.objects.create_user(
                username=username,
                email=email,
                password=password,  # Django gère automatiquement le hachage
                telephone=telephone,
                role='employe',  # Rôle par défaut
                is_active=False  # Statut par défaut
            )
            utilisateur.save()

            # Rediriger vers la page de succès ou d'accueil
            return redirect('login')  # Assure-toi que l'URL 'index' est bien configurée

    return render(request, 'signup.html')  # Page d'inscription si pas de POST

def base(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirige vers la page d'accueil ou une autre page
    else:
        form = RegistrationForm()
    return render(request, 'index.html', {'form': form})


from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
                # Afficher le message d'erreur sur la page
                error_message = "Invalid username or password."
        else:
            messages.error(request, "Invalid username or password.")
            error_message = "Invalid username or password."
    else:
        form = AuthenticationForm()

    return render(request, 'index.html', {'form': form, 'error_message': error_message if 'error_message' in locals() else ''})


from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Utilisateur
from .forms import UtilisateurForm

def user_management(request):
    current_user = request.user
    if current_user.is_superuser:
        users = Utilisateur.objects.all()
    else:
        users = Utilisateur.objects.exclude(is_superuser=True)  # Exclure les super utilisateurs pour les non-super utilisateurs

    form = UtilisateurForm()  # Formulaire pour créer un utilisateur

    if request.method == 'POST':
        if 'create_user' in request.POST:
            form = UtilisateurForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('user_management')  # Redirection après la création

        elif 'update_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(Utilisateur, id=user_id)
            form = UtilisateurForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('user_management')  # Redirection après la mise à jour

    context = {
        'users': users,
        'form': form
    }
    return render(request, 'user.html', context)

def edit_user(request, user_id):
    user = get_object_or_404(Utilisateur, id=user_id)
    # Renvoie les informations de l'utilisateur sous forme de JSON
    data = {
        'id': user.id,
        'username': user.username,
        'telephone': user.telephone,
        'email': user.email,
        'role': user.role,
    }
    return JsonResponse(data)



from django.shortcuts import redirect

def delete_user(request, user_id):
    user = get_object_or_404(Utilisateur, id=user_id)
    user.delete()
    return redirect('user_management')


from django.shortcuts import render, get_object_or_404, redirect
from .models import CategorieProduit
from .forms import CategorieForm

def category_management(request):
    categories = CategorieProduit.objects.all()

    # Pour la création ou la modification de catégorie
    if request.method == 'POST':
        if 'create_category' in request.POST:
            form = CategorieForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('category_management')
        elif 'update_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(CategorieProduit, id=category_id)
            form = CategorieForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return redirect('category_management')
    
    # Formulaire de création vide
    form = CategorieForm()

    return render(request, 'category.html', {
        'categories': categories,
        'form': form,
    })

# Vue pour supprimer une catégorie
def delete_category(request, category_id):
    category = get_object_or_404(CategorieProduit, id=category_id)
    category.delete()
    return redirect('category_management')


# Vue pour se deconnecter
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('login')  # Redirige vers la page de connexion ou d'accueil


#vue produit
from django.shortcuts import render, get_object_or_404, redirect
from .models import Produit, CategorieProduit
from .forms import ProduitForm
from django.utils import timezone

def produits_view(request):
    produits = Produit.objects.all()
    categories = CategorieProduit.objects.all()

    if request.method == 'POST':
        if 'creer_produit' in request.POST:
            # Création d'un produit
            form = ProduitForm(request.POST)
            if form.is_valid():
                produit = form.save(commit=False)
                produit.date_creation = timezone.now()
                produit.save()
                return redirect('produits_view')
            else:
                print(form.errors)

        elif 'modifier_produit' in request.POST:
            # Modification d'un produit existant
            produit_id = request.POST.get('produit_id')
            produit = get_object_or_404(Produit, id=produit_id)
            form = ProduitForm(request.POST, instance=produit)
            if form.is_valid():
                form.save()
                return redirect('produits_view')
            else:
                print(form.errors)

        elif 'supprimer_produit' in request.POST:
            produit_id = request.POST.get('produit_id')
            produit = get_object_or_404(Produit, id=produit_id)
            produit.delete()
            return redirect('produits_view')

    return render(request, 'produit.html', {
        'produits': produits,
        'categories': categories,
    })

#vente cash




from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit, Vente, VenteProduit, Client, Facture
from .forms import ClientForm, VenteForm
from django.db.models import F
import uuid

def vente(request, vente_id):
    vente = get_object_or_404(Vente, id=vente_id)
    produits = Produit.objects.filter(quantite_stock__gt=0)
     # Pré-remplir le formulaire du client avec des valeurs par défaut
    client_initial = {
        'nom': 'clientstandart',
        'telephone': '0',
        'CNIB': '0'
    }
    # Si le client existe déjà, charger ses informations, sinon utiliser les valeurs par défaut
    client_form = ClientForm(instance=vente.client if vente.client else None, initial=client_initial)
    vente_form = VenteForm(instance=vente)

    if request.method == 'POST':
        client_form = ClientForm(request.POST, instance=vente.client)
        vente_form = VenteForm(request.POST, instance=vente)

        # Vérification de la CNIB avant la sauvegarde du client
        cnib = request.POST.get('CNIB')  # Récupérer la CNIB soumise
        client_exist = None
        if cnib:
            try:
                # Récupérer le client existant avec cette CNIB
                client_exist = Client.objects.get(CNIB=cnib)
                vente.client = client_exist  # Associer le client existant à la vente
            except Client.DoesNotExist:
                # Si le client n'existe pas, il sera créé via le formulaire
                if client_form.is_valid():
                    nouveau_client = client_form.save(commit=False)
                    nouveau_client.CNIB = cnib  # Assigner la CNIB au nouveau client
                    nouveau_client.save()
                    vente.client = nouveau_client  # Associer le nouveau client à la vente
        else:
            # Si la CNIB n'est pas fournie, on continue avec le formulaire classique
            if client_form.is_valid():
                client_form.save()

        if vente_form.is_valid():
            if vente.type_paiement == 'credit':
                vente.etait_credits=True
            vente_form.save()

            # Récupérer les produits vendus et leurs détails depuis le POST
            produits_vendus = request.POST.getlist('produits_vendus')  # Liste d'ID des produits
            quantites_vendues = request.POST.getlist('quantites_vendues')  # Liste de quantités
            rabais_produits = request.POST.getlist('rabais_produits')  # Liste de rabais
            prix_totaux = request.POST.getlist('prix_totaux')  # Liste de prix totaux

            total_rabais = 0
            total_encaisse = 0

            for produit_id, quantite, rabais, prix_total in zip(produits_vendus, quantites_vendues, rabais_produits, prix_totaux):
                produit = get_object_or_404(Produit, id=produit_id)
                quantite = int(quantite)
                if not rabais:
                    rabais = 0.0
                else:
                    rabais = float(rabais)

                prix_total = float(prix_total)

                VenteProduit.objects.create(
                    vente=vente,
                    produit=produit,
                    quantite_vendue=quantite,
                    rabais_produit=rabais,
                    prix_total=prix_total
                )

                # Mise à jour du stock
                produit.quantite_stock = F('quantite_stock') - quantite
                produit.save()

                total_rabais += rabais * quantite
                total_encaisse += prix_total

            vente.total_rabais = total_rabais
            vente.total_encaisse = total_encaisse

            # Ajouter au crédit du client si le paiement est à crédit
            if vente.type_paiement == 'credit':
                if client_exist:
                    # Si le client existe déjà, ajouter le montant au crédit actuel
                    client_exist.total_credit = F('total_credit') + total_encaisse
                    client_exist.save()
                else:
                    # Si c'est un nouveau client, utiliser l'instance actuelle
                    vente.client.total_credit = F('total_credit') + total_encaisse
                    vente.client.save()

            vente.save()

            # Générer une facture
            numero_facture = f"FAC-{uuid.uuid4().hex[:8]}"  # Générer un numéro unique pour la facture
            facture = Facture.objects.create(
                vente=vente,
                numero=numero_facture
            )

            # Exemple pour générer un fichier PDF
            # chemin_pdf = generer_facture_pdf(facture)
            # facture.fichier_pdf = chemin_pdf
            # facture.save()

            return redirect('facture', vente_id=vente.id)

    return render(request, 'vente.html', {
        'produits': produits,
        'client_form': client_form,
        'vente_form': vente_form,
    })


def facture(request, vente_id):
    vente = get_object_or_404(Vente, id=vente_id)
    produits = VenteProduit.objects.filter(vente=vente)
    return render(request, 'facture.html', {
        'vente': vente,
        'produits': produits,
    })

from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Vente

def creer_vente(request):
    # Obtenez l'heure actuelle
    current_time = timezone.now()

    # Obtenez toutes les ventes du jour pour l'utilisateur courant
    ventes_du_jour = Vente.objects.filter(
        utilisateur=request.user,
        date_vente__date=current_time.date()
    )

    # Déterminez le nombre de ventes faites aujourd'hui et incrémentez
    nombre_ventes_jour = ventes_du_jour.count() + 1

    # Création d'une nouvelle vente avec tous les champs initialisés
    vente = Vente.objects.create(
        utilisateur=request.user,
        type_paiement='cash',  # Valeur par défaut
        total_rabais=0,
        total_encaisse=0,
        nombre_vente_journee=nombre_ventes_jour,  # Incrémenté
        client=None  # Aucun client pour le moment (peut être modifié plus tard)
    )

    # Redirection vers la page vente avec l'ID de la vente
    return redirect(reverse('vente', args=[vente.id]))


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Vente, VenteProduit, Facture
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

import os
from io import BytesIO
import qrcode
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from .models import Vente, VenteProduit, Facture  # Assure-toi d'importer le modèle Facture
from django.core.files.base import ContentFile

def facture(request, vente_id):
    # Récupérer la vente et ses détails
    vente = get_object_or_404(Vente, id=vente_id)
    produits_vendus = VenteProduit.objects.filter(vente=vente)

    if request.method == 'POST':
        # Génération du PDF
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Définir les positions sur le PDF et ajouter les informations
        pdf.drawString(50, height - 50, f"Facture N°: {vente.facture.numero}")
        pdf.drawString(50, height - 80, f"Date de vente: {vente.date_vente.strftime('%d/%m/%Y à %H:%M')}")
        pdf.drawString(50, height - 110, f"Type de paiement: {vente.type_paiement}")
        pdf.drawString(400, height - 50, f"Vendeur: {vente.utilisateur.username}")
        pdf.drawString(400, height - 80, f"Client: {vente.client.nom}")
        pdf.drawString(400, height - 110, f"Téléphone: {vente.client.telephone}")

        # Ajouter un soulignement avant l'en-tête des produits
        pdf.line(50, height - 140, width - 50, height - 140)  # Ligne horizontale
        y = height - 100
        # Affichage des produits
        y_position = height - 160
        pdf.drawString(50, y_position, "Produit")
        pdf.drawString(200, y_position, "Prix Unitaire")
        pdf.drawString(300, y_position, "Quantité")
        pdf.drawString(400, y_position, "Rabais")
        pdf.drawString(500, y_position, "Total")

        y_position -= 30
        produit_details = []  # Pour stocker les détails des produits à ajouter dans le QR code
        for produit_vendu in produits_vendus:
            pdf.drawString(50, y_position, produit_vendu.produit.nom)
            pdf.drawString(200, y_position, str(produit_vendu.produit.prix_unitaire))
            pdf.drawString(300, y_position, str(produit_vendu.quantite_vendue))
            pdf.drawString(400, y_position, str(produit_vendu.rabais_produit))
            pdf.drawString(500, y_position, str(produit_vendu.prix_total))
            
            # Ajouter les informations de chaque produit à la liste des détails
            produit_details.append(
                f"{produit_vendu.produit.nom}: {produit_vendu.quantite_vendue} x {produit_vendu.produit.prix_unitaire} - Rabais: {produit_vendu.rabais_produit} - Total: {produit_vendu.prix_total} f"
            )
            y_position -= 30

        # Ajouter un soulignement avant le total rabais
        pdf.line(50, y_position - 15, width - 50, y_position - 15)  # Ligne horizontal
        
        # Ajouter le rabais total et le montant encaissé
        pdf.drawString(50, y_position - 30, f"Rabais total: {vente.total_rabais}")
        pdf.drawString(50, y_position - 60, f"Montant total encaissé: {vente.total_encaisse}")

        # Générer les données de la facture avec les produits à inclure dans le QR code
        qr_data = (
            f"Facture N°: {vente.facture.numero}\n"
            f"Client: {vente.client.nom}\n"
            f"Vendeur: {vente.utilisateur.username}\n"  # Ajouter le vendeur ici
            f"Montant Total: {vente.total_encaisse} f\n"
            f"Date: {vente.date_vente.strftime('%d/%m/%Y')}\n\nProduits:\n"
        )
        qr_data += "\n".join(produit_details)  # Ajouter les détails des produits

        # Générer le code QR
        qr_img = qrcode.make(qr_data)
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)

        # Convertir l'image QR en un format utilisable par ReportLab
        qr_image = ImageReader(qr_buffer)

        # Ajouter le QR code au bas du PDF
        pdf.drawImage(qr_image, 50, 50, width=100, height=100)  # Place le QR code en bas de la page

        pdf.save()
        buffer.seek(0)

        # Sauvegarder le PDF dans le champ fichier_pdf de la table Facture
        facture_instance = vente.facture  # Assurez-vous que l'instance de facture existe déjà
        facture_instance.fichier_pdf.save(f'facture_{vente.facture.numero}.pdf', ContentFile(buffer.getvalue()))
        facture_instance.save()

        # Préparer la réponse pour télécharger le PDF
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="facture_{vente.facture.numero}.pdf"'

        return response  # Télécharge le PDF

    # Si ce n'est pas un POST, affiche la page de la facture
    return render(request, 'facture.html', {'vente': vente, 'produits_vendus': produits_vendus})


import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse
from xhtml2pdf import pisa
from .models import Vente, Facture


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')

    # Teste si la génération du PDF échoue
    pdf = pisa.pisaDocument(html.encode('UTF-8'), dest=result, encoding='UTF-8')
    if pdf.err:
        print(f"Erreur dans la génération du PDF : {pdf.err}")  # Ajoute un message pour voir l'erreur
        return None

    return result

def generate_facture_pdf(vente_id):
    vente = Vente.objects.get(id=vente_id)
    produits_vendus = vente.produitvendu_set.all()

    context = {
        'vente': vente,
        'produits_vendus': produits_vendus,
    }

    template_path = 'facture_template.html'  # Template pour la facture
    pdf = render_to_pdf(template_path, context)

    if pdf:
        # Nommer le fichier en fonction du numéro de facture
        filename = f"Facture_{vente.facture.numero}.pdf"
        pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'factures', filename)

        # Créer le dossier 'factures' s'il n'existe pas
        os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)

        # Sauvegarder le fichier PDF
        with open(pdf_file_path, 'wb') as pdf_file:
            pdf_file.write(pdf.content)

        # Sauvegarder le chemin du fichier dans la base de données
        facture = vente.facture
        facture.fichier_pdf = f'factures/{filename}'
        facture.save()

        return pdf_file_path
    return None



from django.http import HttpResponse, Http404
import os


def telecharger_facture_pdf(request, facture_id):
    try:
        # Récupérer la facture avec le fichier PDF
        facture = Facture.objects.get(id=facture_id)

        # Vérifier si le fichier PDF existe
        if facture.fichier_pdf and os.path.exists(facture.fichier_pdf.path):
            # Ouvrir le fichier en mode binaire
            with open(facture.fichier_pdf.path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                # Définir l'en-tête Content-Disposition pour forcer le téléchargement
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(facture.fichier_pdf.name)}"'
                return response
        else:
            raise Http404("Le fichier PDF n'existe pas.")

    except Facture.DoesNotExist:
        raise Http404("Facture non trouvée.")


def liste_factures(request):
    factures = Facture.objects.all().order_by('-vente__date_vente')  
    return render(request, 'liste_facture.html', {'factures': factures})


#vu produit critique voir context_processors.py  et setting pour detail
from django.db.models import F
from .models import Produit

def produits_critiques(request):
    # Filtre des produits critiques
    produits_critiques = Produit.objects.filter(quantite_stock__lte=F('seuil_critique'))
    
    # Compte des produits critiques
    nombre_produits_critiques = produits_critiques.count()

    return render(request, 'ProduitCritiques.html', {
        'produits_critiques': produits_critiques,
        'nombre_produits_critiques': nombre_produits_critiques
    })

#pdf critique products
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from .models import Produit
from django.db.models import F

def telecharger_produits_critiques_pdf(request):
    # Créer un fichier en mémoire
    buffer = io.BytesIO()

    # Définir la taille du document
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Centrer le texte en italique pour "Liste des produits critiques"
    text = "Liste des produits à commander"
    p.setFont("Helvetica-Oblique", 16)  # Police en italique
    text_width = p.stringWidth(text, "Helvetica-Oblique", 16)

    # Positionner le texte centré
    p.drawString((width - text_width) / 2, height - 50, text)

    # Ajouter une ligne pour le soulignement
    p.line((width - text_width) / 2, height - 55, (width + text_width) / 2, height - 55)

    # Saut de ligne
    y = height - 100

    # Ajouter les sous-titres centrés pour les colonnes "Nom du produit" et "Stock actuel"
    p.setFont("Helvetica-BoldOblique", 12)
    p.drawString(100, y, "Nom du produit")
    p.drawString(300, y, "Stock actuel")

    # Souligner les titres
    p.line(100, y - 5, 200, y - 5)  # Ligne sous le titre "Nom du produit"
    p.line(300, y - 5, 400, y - 5)  # Ligne sous le titre "Stock actuel"

    y -= 30  # Sauter une ligne

    # Récupérer les produits critiques
    produits_critiques = Produit.objects.filter(quantite_stock__lte=F('seuil_critique'))

    # Remplir les informations de chaque produit
    for produit in produits_critiques:
        p.setFont("Helvetica", 10)
        p.drawString(100, y, produit.nom)
        p.drawString(300, y, str(produit.quantite_stock))
        y -= 20  # Aller à la ligne suivante

    # Finaliser le PDF
    p.showPage()
    p.save()

    # Réinitialiser le pointeur de mémoire pour que FileResponse puisse lire depuis le début
    buffer.seek(0)

    # Retourner la réponse PDF
    return FileResponse(buffer, as_attachment=True, filename='produits_critiques.pdf')

###Historique
from django.shortcuts import render, get_object_or_404
from .models import Vente

def historique(request):
    # Récupérer toutes les ventes triées par date (les plus récentes d'abord)
    ventes = Vente.objects.all().order_by('-date_vente')
    return render(request, 'historique.html', {'ventes': ventes})

def historique_detail(request, vente_id):
    # Récupérer les détails d'une vente spécifique
    vente = get_object_or_404(Vente, id=vente_id)
    produits = VenteProduit.objects.filter(vente=vente)  # Obtenir les produits vendus pour cette vente

    # Calculer le total pour chaque produit si ce n'est pas déjà fait
    for produit in produits:
        produit.prix_total = produit.produit.prix_unitaire * produit.quantite_vendue - produit.rabais_produit

    return render(request, 'historiquedetail.html', {'vente': vente, 'produits': produits})

# Rapport journalier
from django.shortcuts import render
from django.utils import timezone
from .models import Vente, VenteProduit
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.db.models import Sum

def rapport_jour(request):
    # Obtenir la date actuelle
    today = timezone.now().date()

    # Obtenir toutes les ventes du jour (y compris celles à crédit)
    ventes_jour = Vente.objects.filter(date_vente__date=today)

    # Obtenir tous les produits vendus dans la journée (en incluant les ventes à crédit)
    produits_vendus = VenteProduit.objects.filter(vente__in=ventes_jour).values(
        'produit__nom', 'produit__prix_achat'
    ).annotate(
        quantite_vendue_jour=Sum('quantite_vendue'),  # Total des quantités vendues (y compris crédit)
    )

    # Filtrer uniquement les ventes en cash pour les calculs
    ventes_en_cash = ventes_jour.filter(type_paiement='cash')

    # Calcul du chiffre d'affaires total uniquement pour les ventes en cash
    chiffre_affaire_total = ventes_en_cash.aggregate(total_encaisse=Sum('total_encaisse'))['total_encaisse'] or 0

    # Calcul du coût total des produits vendus en cash
    cout_total = sum(
        p['produit__prix_achat'] * VenteProduit.objects.filter(vente__in=ventes_en_cash, produit__nom=p['produit__nom']).aggregate(Sum('quantite_vendue'))['quantite_vendue__sum'] 
        for p in produits_vendus
    )

    # Calcul du bénéfice total en fonction des ventes en cash
    benefice_total = chiffre_affaire_total - cout_total

    # Vérifier si on demande un rapport PDF
    if request.GET.get('format') == 'pdf':
        return generer_pdf(ventes_en_cash, produits_vendus, chiffre_affaire_total, benefice_total)

    return render(request, 'rapportjour.html', {
        'produits_vendus': produits_vendus,
        'chiffre_affaire_total': chiffre_affaire_total,
        'benefice_total': benefice_total,
        'today': today  # Ajout de la date actuelle au contexte pour la date
    })

from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from django.http import HttpResponse
from django.utils import timezone

def generer_pdf(ventes_jour, produits_vendus, chiffre_affaire_total, benefice_total):
    # Création du PDF
    response = HttpResponse(content_type='application/pdf')
    
    # Formatage de la date pour le nom de fichier
    today_date = timezone.now().date().strftime("%Y-%m-%d")  # Format: AAAA-MM-JJ
    response['Content-Disposition'] = f'attachment; filename="rapport_jour_{today_date}.pdf"'
    
    # Initialisation de la page PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Charger une police standard (par exemple, Helvetica-Bold)
    p.setFont("Helvetica-Bold", 16)

    # Titre du rapport centré et souligné
    p.drawCentredString(width / 2, height - 100, f"Rapport des ventes du {timezone.now().date()}")
    p.line(100, height - 105, width - 100, height - 105)  # Soulignement du titre

    # Titre des colonnes en gras
    y_position = height - 160
    p.setFont("Helvetica-Bold", 12)

    # Titre "Produits vendus"
    p.drawString(100, y_position, "Produits vendus :")
    p.line(100, y_position - 5, 200, y_position - 5)  # Souligner "Produits vendus"

    y_position -= 20

    # Titres des colonnes "Nom(s) produits" et "Quantité vendue"
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y_position, "Nom(s) produits")
    p.drawRightString(width - 100, y_position, "Quantité vendue (y compris à crédit)")

    y_position -= 20
    p.setFont("Helvetica", 12)

    # Boucle pour afficher les produits vendus
    for produit in produits_vendus:
        # Sauter à la page suivante si la hauteur est trop basse
        if y_position < 50:
            p.showPage()
            y_position = height - 40

            # Réafficher les titres des colonnes sur la nouvelle page
            p.setFont("Helvetica-Bold", 12)
            p.drawString(100, y_position, "Nom(s) produits")
            p.drawRightString(width - 100, y_position, "Quantité vendue (y compris à crédit)")
            y_position -= 20
            p.setFont("Helvetica", 12)

        # Produit à gauche (nom en gras)
        p.drawString(100, y_position, f"{produit['produit__nom']}")
        p.drawRightString(width - 100, y_position, f"{produit['quantite_vendue_jour']}")

        y_position -= 20

    # Sauter une ligne après la liste des produits
    y_position -= 20

    # Vérifier si la hauteur est suffisante pour afficher les montants, sinon sauter à la page suivante
    if y_position < 50:
        p.showPage()
        y_position = height - 40

    # Soulignement avant le chiffre d'affaires et le bénéfice total
    p.line(100, y_position, width - 100, y_position)
    y_position -= 20
    # Affichage du chiffre d'affaires et du bénéfice total après la liste des produits
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y_position, f"Chiffre d'affaires total (en cash) : {chiffre_affaire_total:.2f} FCFA")
    y_position -= 20
    p.drawString(100, y_position, f"Bénéfice total (en cash) : {benefice_total:.2f} FCFA")

    # Sauvegarde du PDF et fin de génération
    p.showPage()
    p.save()

    return response

## rapport mois 
from django.shortcuts import render
from django.utils import timezone
from .models import Vente, VenteProduit
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.db.models import Sum
from datetime import timedelta

def rapport_mois(request):
    # Obtenir la date actuelle
    today = timezone.now().date()

    # Obtenir le premier jour du mois et le dernier jour du mois
    first_day_of_month = today.replace(day=1)
    last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Obtenir toutes les ventes du mois (y compris celles à crédit)
    ventes_mois = Vente.objects.filter(date_vente__date__gte=first_day_of_month, date_vente__date__lte=last_day_of_month)

    # Obtenir tous les produits vendus dans le mois (y compris les ventes à crédit)
    produits_vendus = VenteProduit.objects.filter(vente__in=ventes_mois).values(
        'produit__nom', 'produit__prix_achat'
    ).annotate(
        quantite_vendue_mois=Sum('quantite_vendue')  # Total des quantités vendues
    )

    # Filtrer uniquement les ventes en cash pour les calculs financiers
    ventes_en_cash = ventes_mois.filter(type_paiement='cash')

    # Calcul du chiffre d'affaires total uniquement pour les ventes en cash
    chiffre_affaire_total = ventes_en_cash.aggregate(total_encaisse=Sum('total_encaisse'))['total_encaisse'] or 0

    # Calcul du coût total des produits vendus en cash
    cout_total = sum(
        p['produit__prix_achat'] * VenteProduit.objects.filter(vente__in=ventes_en_cash, produit__nom=p['produit__nom']).aggregate(Sum('quantite_vendue'))['quantite_vendue__sum'] 
        for p in produits_vendus
    )

    # Calcul du bénéfice total en fonction des ventes en cash
    benefice_total = chiffre_affaire_total - cout_total

    # Vérifier si on demande un rapport PDF
    if request.GET.get('format') == 'pdf':
        # Passer les paramètres nécessaires pour la génération du PDF
        return generer_mois_pdf(produits_vendus, chiffre_affaire_total, benefice_total)

    return render(request, 'rapportmois.html', {
        'produits_vendus': produits_vendus,
        'chiffre_affaire_total': chiffre_affaire_total,
        'benefice_total': benefice_total,
        'first_day_of_month': first_day_of_month,
        'last_day_of_month': last_day_of_month,
        'today': today,
        'mois': first_day_of_month,
    })



from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.utils import timezone

def generer_mois_pdf(produits_vendus, chiffre_affaire_total, benefice_total):
    # Création du PDF
    response = HttpResponse(content_type='application/pdf')

    # Formatage de la date pour le nom de fichier
    today_date = timezone.now().date().strftime("%Y-%m-%d")  # Format: AAAA-MM-JJ
    response['Content-Disposition'] = f'attachment; filename="rapport_mois_{today_date}.pdf"'

    # Initialisation de la page PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Charger une police standard (par exemple, Helvetica-Bold)
    p.setFont("Helvetica-Bold", 16)

    # Titre du rapport centré et souligné
    p.drawCentredString(width / 2, height - 100, f"Rapport des ventes pour le mois de {timezone.now().strftime('%B %Y')}")
    p.line(100, height - 105, width - 100, height - 105)  # Soulignement du titre

    # Titre des colonnes en gras
    y_position = height - 160
    p.setFont("Helvetica-Bold", 12)

    # Titre "Produits vendus"
    p.drawString(100, y_position, "Produits vendus :")
    p.line(100, y_position - 5, 200, y_position - 5)  # Souligner "Produits vendus"

    y_position -= 20

    # Titres des colonnes "Nom(s) produits" et "Quantité vendue"
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y_position, "Nom(s) produits")
    p.drawRightString(width - 100, y_position, "Quantité vendue (y compris à crédit)")

    y_position -= 20
    p.setFont("Helvetica", 12)

    # Boucle pour afficher les produits vendus durant le mois
    for produit in produits_vendus:
        # Sauter à la page suivante si la hauteur est trop basse
        if y_position < 50:
            p.showPage()
            y_position = height - 40

            # Réafficher les titres des colonnes sur la nouvelle page
            p.setFont("Helvetica-Bold", 12)
            p.drawString(100, y_position, "Nom(s) produits")
            p.drawRightString(width - 100, y_position, "Quantité vendue (y compris à crédit)")
            y_position -= 20
            p.setFont("Helvetica", 12)

        # Produit à gauche (nom en gras)
        p.drawString(100, y_position, f"{produit['produit__nom']}")
        p.drawRightString(width - 100, y_position, f"{produit['quantite_vendue_mois']}")

        y_position -= 20

    # Sauter une ligne après la liste des produits
    y_position -= 20

    # Vérifier si la hauteur est suffisante pour afficher les montants, sinon sauter à la page suivante
    if y_position < 50:
        p.showPage()
        y_position = height - 40

    # Soulignement avant le chiffre d'affaires et le bénéfice total
    p.line(100, y_position, width - 100, y_position)
    y_position -= 20

    # Affichage du chiffre d'affaires et du bénéfice total après la liste des produits
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y_position, f"Chiffre d'affaires total (en cash) pour le mois : {chiffre_affaire_total:.2f} FCFA")
    y_position -= 20
    p.drawString(100, y_position, f"Bénéfice total (en cash) pour le mois : {benefice_total:.2f} FCFA")

    # Sauvegarde du PDF et fin de génération
    p.showPage()
    p.save()

    return response

from django.shortcuts import render

# Vue pour la page "About Us"
def about_us(request):
    return render(request, 'about.html')

from django.shortcuts import render
from .models import Vente, Produit, Utilisateur, VenteProduit
from django.db.models import Sum
from datetime import datetime

def homes_view(request):
    # Filtrer les ventes de la journée
    today = datetime.today().date()
    
    # Compter le nombre de ventes de la journée
    ventes_journee = Vente.objects.filter(date_vente__date=today).count()
    
    # Compter le nombre total d'utilisateurs
    total_utilisateurs = Utilisateur.objects.count()
    
    # Calculer le chiffre d'affaire total (des ventes en cash) de la journée
    ventes_en_cash = Vente.objects.filter(
        date_vente__date=today,
        type_paiement='cash'
    )
    
    chiffre_affaire_total = ventes_en_cash.aggregate(Sum('total_encaisse'))['total_encaisse__sum'] or 0

    # Récupérer les produits vendus et leurs prix d'achat
    produits_vendus = VenteProduit.objects.filter(vente__in=ventes_en_cash).values('produit__nom', 'produit__prix_achat').annotate(total_vendu=Sum('quantite_vendue'))

    # Calculer le coût total
    cout_total = sum(
        p['produit__prix_achat'] * p['total_vendu'] 
        for p in produits_vendus
    )

    # Calculer le bénéfice total en fonction des ventes en cash
    benefice_total = chiffre_affaire_total - cout_total

    # Récupérer les données pour l'histogramme (nombre de ventes par produit)
    produits = [p['produit__nom'] for p in produits_vendus]
    quantites = [p['total_vendu'] for p in produits_vendus]

    # Récupérer les données pour le diagramme circulaire (ventes en cash et crédit)
    ventes_credit = Vente.objects.filter(date_vente__date=today, type_paiement='credit').count()

    context = {
        'ventes_journee': ventes_journee,
        'total_utilisateurs': total_utilisateurs,
        'chiffre_affaire_total': chiffre_affaire_total,
        'benefice_total': benefice_total,
        'produits': produits,
        'quantites': quantites,
        'ventes_cash': ventes_en_cash.count(),
        'ventes_credit': ventes_credit,
    }

    return render(request, 'home.html', context)



from .models import Vente, Credits

import os
from django.conf import settings
from django.http import JsonResponse, Http404
from django.utils import timezone
from reportlab.pdfgen import canvas
from .models import Vente, Credits, Client  # Assurez-vous que ces modèles sont importés

def confirmer_paiement(request):
    vente_id = request.GET.get('vente_id')
    vente = Vente.objects.filter(id=vente_id).first()

    if vente is None:
        raise Http404("Vente introuvable")

    # Vérifiez si le paiement est bien en crédit
    if vente.type_paiement == 'credit':
        # Mettre à jour le type de paiement
        vente.type_paiement = 'cash'
        vente.save()

        # Mettre à jour le champ total_credit du client
        client = vente.client
        montant_paye = vente.total_encaisse
        client.total_credit -= montant_paye
        client.save()

        # Créer une instance de Credits pour cette vente
        credit = Credits.objects.create(
            vente=vente,
            date_paiement=timezone.now(),
            montant=montant_paye,
        )

        # Définir le chemin et le nom du fichier PDF
        pdf_filename = f"Facture_Credit_Paye_{vente.id}.pdf"
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'factures', pdf_filename)

        # Créer et enregistrer le PDF
        with open(pdf_path, "wb") as pdf_file:
            p = canvas.Canvas(pdf_file)
            p.drawString(100, 750, f"Facture Crédit Payé - numéro de facture: {vente.facture.numero}")
            p.drawString(100, 725, f"Date de Paiement: {credit.date_paiement.strftime('%Y-%m-%d')}")
            p.drawString(100, 700, f"Client: {client.nom}")
            p.drawString(100, 675, f"CNIB: {client.CNIB}")
            p.drawString(100, 650, f"Montant Total: {vente.total_encaisse} f")
            p.drawString(100, 625, f"Montant Payé: {credit.montant} f")
            p.drawString(100, 600, f"Utilisateur: {vente.utilisateur.username}")
            p.showPage()
            p.save()

        # Enregistrer le chemin du fichier PDF dans l'instance de Credits
        credit.pdf.name = f"factures/{pdf_filename}"
        credit.save()

        # Réponse JSON avec succès
        return JsonResponse({'success': True})

    # Si le paiement n'est pas en crédit ou est déjà payé
    return JsonResponse({'success': False, 'message': 'Le paiement n\'est pas en crédit ou est déjà payé.'}, status=400)

from django.shortcuts import render
from django.db.models import Count
from .models import Client, Vente

def liste_clients(request):
    # Récupérer les clients avec le nombre d'achats
    clients = Client.objects.annotate(nombre_achats=Count('vente')).order_by('-nombre_achats')

    # Passer les données des clients à la template
    return render(request, 'client.html', {'clients': clients})


from django.shortcuts import get_object_or_404, redirect
# Remplace par ton modèle d'utilisateur personnalisé si ce n'est pas le modèle par défaut de Django
from .models import Utilisateur  

def toggle_user_status(request, user_id):
    # Remplace 'User' par 'Utilisateur' ou ton modèle d'utilisateur si tu utilises un modèle personnalisé
    user = get_object_or_404(Utilisateur, id=user_id)
    user.is_active = not user.is_active  # Inverse la valeur actuelle
    user.save()
    return redirect('user_management')  # Redirection vers la page de gestion des utilisateurs
