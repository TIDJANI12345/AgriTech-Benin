from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.accueil, name='accueil'),
    
    # Déconnexion personnalisée
    path('logout/', views.custom_logout, name='logout'),
    
    # URLs pour les Producteurs
    path('producteur/dashboard/', views.dashboard_producteur, name='dashboard_producteur'),
    path('producteur/mes-recoltes/', views.mes_recoltes, name='mes_recoltes'),
    path('producteur/ajouter-recolte/', views.ajouter_recolte, name='ajouter_recolte'),
    
    # URLs pour les Gestionnaires
    path('gestionnaire/dashboard/', views.dashboard_gestionnaire, name='dashboard_gestionnaire'),
    path('gestionnaire/stocks/', views.gestion_stocks, name='gestion_stocks'),
    path('gestionnaire/stocks/modifier/<int:entrepot_id>/', views.modifier_stock, name='modifier_stock'),
    path('gestionnaire/recoltes/', views.toutes_recoltes, name='toutes_recoltes'),
    
    # Health check pour les cron jobs
    path('health/', views.health_check, name='health_check'),
]