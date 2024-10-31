from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import register,login_view,produits_view,telecharger_facture_pdf

urlpatterns = [
    
    path('base/', views.base, name='base'),
    path('register/', register, name='register'),
    path('porgo/', views.signup_view, name='signup'),
    path('', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('users/', views.user_management, name='user_management'),
    path('user/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user/toggle/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),

    path('categories/', views.category_management, name='category_management'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),

    path('produits/', produits_view, name='produits_view'),
    path('vente/<int:vente_id>/', views.vente, name='vente'),
    path('creer_vente/', views.creer_vente, name='creer_vente'),
    
    path('facture/<int:vente_id>/', views.facture, name='facture'),
    path('facture/telecharger/<int:vente_id>/', telecharger_facture_pdf, name='telecharger_facture'),
    path('factures/', views.liste_factures, name='liste_factures'),

    path('produits-critiques/', views.produits_critiques, name='produits_critiques'),
    path('telecharger-produits-critiques/', views.telecharger_produits_critiques_pdf, name='telecharger_produits_critiques'),

    path('historique/', views.historique, name='historique'),
    path('historique/<int:vente_id>/', views.historique_detail, name='historique_detail'),


    path('generer_pdf/', views.generer_pdf, name='generer_pdf'),
    path('rapport_jour/', views.rapport_jour, name='rapport_jour'),

    path('generer_mois_pdf/', views.generer_mois_pdf, name='generer_mois_pdf'),
    path('rapport_mois/', views.rapport_mois, name='rapport_mois'),

    path('about-us/', views.about_us, name='about_us'),
    path('home/', views.homes_view, name='home'),

    path('confirmer_paiement/', views.confirmer_paiement, name='confirmer_paiement'),


    path('clients/', views.liste_clients, name='liste_clients'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
