from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Sum, Q
from .models import (
    Producteur, Parcelle, Recolte, TypeCulture, 
    Entrepot, Stock, Arrondissement, Commune
)
from .forms import RecolteForm, StockForm

from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse

def health_check(request):
    """Endpoint simple pour les health checks"""
    return HttpResponse("OK", status=200)

# ============================================
# VUES POUR LES PRODUCTEURS
# ============================================

def custom_logout(request):
    """Déconnecte l'utilisateur et redirige vers l'accueil"""
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès. À bientôt !")
    return redirect('accueil')

@login_required
def dashboard_producteur(request):
    """Tableau de bord du producteur - Voit uniquement ses données"""
    try:
        producteur = request.user.producteur
    except Producteur.DoesNotExist:
        messages.error(request, "Vous n'êtes pas enregistré comme producteur.")
        return redirect('admin:index')
    
    # Statistiques du producteur
    mes_parcelles = producteur.parcelles.all()
    mes_recoltes = Recolte.objects.filter(parcelle__producteur=producteur)
    
    # Total des récoltes par type de culture
    recoltes_par_culture = mes_recoltes.values('type_culture__nom').annotate(
        total=Sum('quantite')
    ).order_by('-total')
    
    # Dernières récoltes
    dernieres_recoltes = mes_recoltes.order_by('-date_recolte')[:5]
    
    context = {
        'producteur': producteur,
        'nombre_parcelles': mes_parcelles.count(),
        'nombre_recoltes': mes_recoltes.count(),
        'recoltes_par_culture': recoltes_par_culture,
        'dernieres_recoltes': dernieres_recoltes,
        'total_recolte': mes_recoltes.aggregate(Sum('quantite'))['quantite__sum'] or 0,
    }
    
    return render(request, 'gestion/dashboard_producteur.html', context)


@login_required
def mes_recoltes(request):
    """Liste des récoltes du producteur connecté"""
    try:
        producteur = request.user.producteur
    except Producteur.DoesNotExist:
        messages.error(request, "Vous n'êtes pas enregistré comme producteur.")
        return redirect('admin:index')
    
    recoltes = Recolte.objects.filter(parcelle__producteur=producteur).order_by('-date_recolte')
    
    context = {
        'recoltes': recoltes,
        'producteur': producteur,
    }
    
    return render(request, 'gestion/mes_recoltes.html', context)


@login_required
@permission_required('gestion.add_recolte', raise_exception=True)
def ajouter_recolte(request):
    """Permet au producteur d'ajouter une récolte"""
    try:
        producteur = request.user.producteur
    except Producteur.DoesNotExist:
        messages.error(request, "Vous n'êtes pas enregistré comme producteur.")
        return redirect('admin:index')
    
    if request.method == 'POST':
        form = RecolteForm(request.POST, producteur=producteur)
        if form.is_valid():
            recolte = form.save()
            messages.success(request, f"Récolte de {recolte.quantite}kg de {recolte.type_culture} enregistrée avec succès !")
            return redirect('mes_recoltes')
    else:
        form = RecolteForm(producteur=producteur)
    
    context = {
        'form': form,
        'producteur': producteur,
    }
    
    return render(request, 'gestion/ajouter_recolte.html', context)


# ============================================
# VUES POUR LES GESTIONNAIRES
# ============================================

@login_required
@permission_required('gestion.view_stock', raise_exception=True)
def dashboard_gestionnaire(request):
    """Tableau de bord du gestionnaire - Voit tout"""
    
    # Statistiques globales
    total_producteurs = Producteur.objects.filter(actif=True).count()
    total_recoltes = Recolte.objects.count()
    total_entrepots = Entrepot.objects.count()
    
    # Entrepôts avec alertes
    entrepots_alerte = [e for e in Entrepot.objects.all() if e.alerte_stock_bas]
    
    # Stock total par type de culture
    stocks_par_culture = Stock.objects.values('type_culture__nom').annotate(
        total=Sum('quantite')
    ).order_by('-total')
    
    # Récoltes récentes
    recoltes_recentes = Recolte.objects.select_related(
        'parcelle__producteur__user', 'type_culture'
    ).order_by('-date_recolte')[:10]
    
    # Production par arrondissement
    production_par_zone = Recolte.objects.values(
        'parcelle__arrondissement__nom',
        'parcelle__arrondissement__commune__nom'
    ).annotate(
        total=Sum('quantite')
    ).order_by('-total')[:5]
    
    context = {
        'total_producteurs': total_producteurs,
        'total_recoltes': total_recoltes,
        'total_entrepots': total_entrepots,
        'entrepots_alerte': entrepots_alerte,
        'nombre_alertes': len(entrepots_alerte),
        'stocks_par_culture': stocks_par_culture,
        'recoltes_recentes': recoltes_recentes,
        'production_par_zone': production_par_zone,
    }
    
    return render(request, 'gestion/dashboard_gestionnaire.html', context)


@login_required
@permission_required('gestion.view_stock', raise_exception=True)
def gestion_stocks(request):
    """Vue de gestion des stocks pour les gestionnaires"""
    entrepots = Entrepot.objects.all()
    
    # Calculer les alertes pour chaque entrepôt
    for entrepot in entrepots:
        entrepot.alerte = entrepot.alerte_stock_bas
        entrepot.stock_total = entrepot.stock_actuel
        entrepot.taux = entrepot.taux_remplissage
    
    context = {
        'entrepots': entrepots,
    }
    
    return render(request, 'gestion/gestion_stocks.html', context)


@login_required
@permission_required('gestion.change_stock', raise_exception=True)
def modifier_stock(request, entrepot_id):
    """Permet au gestionnaire de modifier les stocks d'un entrepôt"""
    entrepot = get_object_or_404(Entrepot, id=entrepot_id)
    stocks = Stock.objects.filter(entrepot=entrepot)
    
    if request.method == 'POST':
        form = StockForm(request.POST, entrepot=entrepot)
        if form.is_valid():
            stock = form.save()
            messages.success(request, f"Stock de {stock.type_culture} mis à jour : {stock.quantite}kg")
            return redirect('gestion_stocks')
    else:
        form = StockForm(entrepot=entrepot)
    
    context = {
        'entrepot': entrepot,
        'stocks': stocks,
        'form': form,
    }
    
    return render(request, 'gestion/modifier_stock.html', context)


@login_required
@permission_required('gestion.view_recolte', raise_exception=True)
def toutes_recoltes(request):
    """Liste de toutes les récoltes (pour gestionnaires)"""
    recoltes = Recolte.objects.select_related(
        'parcelle__producteur__user', 
        'type_culture',
        'parcelle__arrondissement'
    ).order_by('-date_recolte')
    
    # Filtres
    type_culture = request.GET.get('type_culture')
    arrondissement = request.GET.get('arrondissement')
    
    if type_culture:
        recoltes = recoltes.filter(type_culture__nom=type_culture)
    
    if arrondissement:
        recoltes = recoltes.filter(parcelle__arrondissement__id=arrondissement)
    
    context = {
        'recoltes': recoltes,
        'types_cultures': TypeCulture.objects.all(),
        'arrondissements': Arrondissement.objects.all(),
        'type_culture_filtre': type_culture,
        'arrondissement_filtre': arrondissement,
    }
    
    return render(request, 'gestion/toutes_recoltes.html', context)


# ============================================
# VUE PUBLIQUE
# ============================================

def accueil(request):
    """Page d'accueil du site"""
    try:
        if request.user.is_authenticated:
            # Rediriger selon le type d'utilisateur
            try:
                if hasattr(request.user, 'producteur') and request.user.producteur:
                    return redirect('dashboard_producteur')
            except Producteur.DoesNotExist:
                pass
            
            if request.user.groups.filter(name='Gestionnaire').exists():
                return redirect('dashboard_gestionnaire')
            
            # Si authentifié mais ni producteur ni gestionnaire
            return redirect('admin:index')
        
        # Statistiques publiques
        context = {
            'total_producteurs': Producteur.objects.filter(actif=True).count(),
            'total_communes': Commune.objects.count(),
            'total_recoltes_kg': Recolte.objects.aggregate(Sum('quantite'))['quantite__sum'] or 0,
        }
        
        return render(request, 'gestion/accueil.html', context)
    
    except Exception as e:
        # En cas d'erreur, afficher un message de debug
        from django.http import HttpResponse
        return HttpResponse(f"Erreur sur la page d'accueil: {str(e)}<br><br>Allez sur <a href='/admin/'>/admin/</a>")