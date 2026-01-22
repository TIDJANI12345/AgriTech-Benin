from django.contrib import admin
from .models import (
    Commune, Arrondissement, Producteur, Parcelle,
    TypeCulture, Recolte, Entrepot, Stock
)

@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'nombre_arrondissements']
    search_fields = ['nom', 'code']
    
    def nombre_arrondissements(self, obj):
        return obj.arrondissements.count()
    nombre_arrondissements.short_description = "Nb Arrondissements"


@admin.register(Arrondissement)
class ArrondissementAdmin(admin.ModelAdmin):
    list_display = ['nom', 'commune', 'code', 'nombre_producteurs', 'nombre_parcelles']
    list_filter = ['commune']
    search_fields = ['nom', 'code', 'commune__nom']
    
    def nombre_producteurs(self, obj):
        return obj.producteurs.count()
    nombre_producteurs.short_description = "Nb Producteurs"
    
    def nombre_parcelles(self, obj):
        return obj.parcelles.count()
    nombre_parcelles.short_description = "Nb Parcelles"


@admin.register(Producteur)
class ProducteurAdmin(admin.ModelAdmin):
    list_display = ['user', 'telephone', 'arrondissement', 'date_inscription', 'actif', 'nombre_parcelles']
    list_filter = ['actif', 'arrondissement__commune', 'date_inscription']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'telephone']
    date_hierarchy = 'date_inscription'
    
    def nombre_parcelles(self, obj):
        return obj.parcelles.count()
    nombre_parcelles.short_description = "Nb Parcelles"


@admin.register(Parcelle)
class ParcelleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'producteur', 'arrondissement', 'superficie', 'latitude', 'longitude']
    list_filter = ['arrondissement__commune', 'arrondissement']
    search_fields = ['nom', 'producteur__user__username', 'producteur__user__first_name']


@admin.register(TypeCulture)
class TypeCultureAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description']
    search_fields = ['nom']


@admin.register(Recolte)
class RecolteAdmin(admin.ModelAdmin):
    list_display = ['type_culture', 'parcelle', 'quantite', 'date_recolte', 'producteur_nom', 'date_enregistrement']
    list_filter = ['type_culture', 'date_recolte', 'parcelle__arrondissement__commune']
    search_fields = ['parcelle__nom', 'parcelle__producteur__user__username']
    date_hierarchy = 'date_recolte'
    
    def producteur_nom(self, obj):
        return obj.producteur
    producteur_nom.short_description = "Producteur"


@admin.register(Entrepot)
class EntrepotAdmin(admin.ModelAdmin):
    list_display = ['nom', 'arrondissement', 'capacite_max', 'seuil_alerte', 'stock_actuel', 'taux_remplissage_pct', 'alerte']
    list_filter = ['arrondissement__commune', 'arrondissement']
    search_fields = ['nom', 'gestionnaire__username']
    
    def taux_remplissage_pct(self, obj):
        return f"{obj.taux_remplissage:.1f}%"
    taux_remplissage_pct.short_description = "Taux Remplissage"
    
    def alerte(self, obj):
        return "⚠️ ALERTE" if obj.alerte_stock_bas else "✅ OK"
    alerte.short_description = "État Stock"


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['entrepot', 'type_culture', 'quantite', 'date_mise_a_jour']
    list_filter = ['entrepot', 'type_culture']
    search_fields = ['entrepot__nom']
    readonly_fields = ['date_mise_a_jour']