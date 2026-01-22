from django import forms
from .models import Recolte, Stock, Parcelle, TypeCulture

class RecolteForm(forms.ModelForm):
    """Formulaire pour enregistrer une récolte"""
    
    class Meta:
        model = Recolte
        fields = ['parcelle', 'type_culture', 'quantite', 'date_recolte']
        widgets = {
            'date_recolte': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'parcelle': forms.Select(attrs={'class': 'form-control'}),
            'type_culture': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité en kg'}),
        }
        labels = {
            'parcelle': 'Parcelle',
            'type_culture': 'Type de culture',
            'quantite': 'Quantité (kg)',
            'date_recolte': 'Date de récolte',
        }
    
    def __init__(self, *args, **kwargs):
        # Récupérer le producteur pour filtrer ses parcelles
        producteur = kwargs.pop('producteur', None)
        super().__init__(*args, **kwargs)
        
        if producteur:
            # Le producteur ne voit que ses propres parcelles
            self.fields['parcelle'].queryset = Parcelle.objects.filter(producteur=producteur)


class StockForm(forms.ModelForm):
    """Formulaire pour modifier le stock d'un entrepôt"""
    
    class Meta:
        model = Stock
        fields = ['type_culture', 'quantite']
        widgets = {
            'type_culture': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantité en kg'}),
        }
        labels = {
            'type_culture': 'Type de culture',
            'quantite': 'Quantité en stock (kg)',
        }
    
    def __init__(self, *args, **kwargs):
        # Récupérer l'entrepôt
        entrepot = kwargs.pop('entrepot', None)
        super().__init__(*args, **kwargs)
        
        self.entrepot = entrepot
    
    def save(self, commit=True):
        stock = super().save(commit=False)
        stock.entrepot = self.entrepot
        
        if commit:
            # Vérifier si un stock existe déjà pour ce type de culture
            existing_stock = Stock.objects.filter(
                entrepot=self.entrepot,
                type_culture=stock.type_culture
            ).first()
            
            if existing_stock:
                # Mettre à jour le stock existant
                existing_stock.quantite = stock.quantite
                existing_stock.save()
                return existing_stock
            else:
                # Créer un nouveau stock
                stock.save()
                return stock
        
        return stock