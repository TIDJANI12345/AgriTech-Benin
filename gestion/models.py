from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Commune(models.Model):
    """Représente une commune au Bénin (ex: Cotonou, Porto-Novo)"""
    nom = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, help_text="Code de la commune")
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Commune"
        verbose_name_plural = "Communes"
    
    def __str__(self):
        return self.nom


class Arrondissement(models.Model):
    """Subdivision administrative d'une commune"""
    nom = models.CharField(max_length=100)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='arrondissements')
    code = models.CharField(max_length=10, help_text="Code de l'arrondissement")
    
    class Meta:
        ordering = ['commune', 'nom']
        verbose_name = "Arrondissement"
        verbose_name_plural = "Arrondissements"
        unique_together = ['nom', 'commune']
    
    def __str__(self):
        return f"{self.nom} ({self.commune.nom})"


class Producteur(models.Model):
    """Agriculteur membre de la coopérative"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='producteur')
    telephone = models.CharField(max_length=20)
    arrondissement = models.ForeignKey(Arrondissement, on_delete=models.SET_NULL, null=True, related_name='producteurs')
    date_inscription = models.DateField(auto_now_add=True)
    actif = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date_inscription']
        verbose_name = "Producteur"
        verbose_name_plural = "Producteurs"
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"
    
    @property
    def nombre_parcelles(self):
        return self.parcelles.count()


class Parcelle(models.Model):
    """Terrain cultivé par un producteur"""
    producteur = models.ForeignKey(Producteur, on_delete=models.CASCADE, related_name='parcelles')
    arrondissement = models.ForeignKey(Arrondissement, on_delete=models.CASCADE, related_name='parcelles')
    superficie = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], help_text="Superficie en hectares")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    nom = models.CharField(max_length=100, help_text="Nom ou identifiant de la parcelle")
    
    class Meta:
        ordering = ['producteur', 'nom']
        verbose_name = "Parcelle"
        verbose_name_plural = "Parcelles"
    
    def __str__(self):
        return f"{self.nom} - {self.producteur}"


class TypeCulture(models.Model):
    """Type de culture (Maïs, Soja, Ananas, etc.)"""
    MAIS = 'MAIS'
    SOJA = 'SOJA'
    ANANAS = 'ANANAS'
    
    TYPES_CHOICES = [
        (MAIS, 'Maïs'),
        (SOJA, 'Soja'),
        (ANANAS, 'Ananas'),
    ]
    
    nom = models.CharField(max_length=50, choices=TYPES_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Type de Culture"
        verbose_name_plural = "Types de Cultures"
    
    def __str__(self):
        return self.get_nom_display()


class Recolte(models.Model):
    """Enregistrement d'une récolte sur une parcelle"""
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE, related_name='recoltes')
    type_culture = models.ForeignKey(TypeCulture, on_delete=models.CASCADE, related_name='recoltes')
    quantite = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Quantité en kg")
    date_recolte = models.DateField()
    date_enregistrement = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_recolte']
        verbose_name = "Récolte"
        verbose_name_plural = "Récoltes"
    
    def __str__(self):
        return f"{self.type_culture} - {self.quantite}kg ({self.date_recolte})"
    
    @property
    def producteur(self):
        return self.parcelle.producteur


class Entrepot(models.Model):
    """Lieu de stockage des récoltes"""
    nom = models.CharField(max_length=100, unique=True)
    arrondissement = models.ForeignKey(Arrondissement, on_delete=models.CASCADE, related_name='entrepots')
    capacite_max = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Capacité maximale en kg")
    seuil_alerte = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Seuil d'alerte de stock bas en kg")
    gestionnaire = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='entrepots_geres')
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Entrepôt"
        verbose_name_plural = "Entrepôts"
    
    def __str__(self):
        return self.nom
    
    @property
    def stock_actuel(self):
        """Calcule le stock total actuel dans l'entrepôt"""
        total = self.stocks.aggregate(total=models.Sum('quantite'))['total']
        return total or 0
    
    @property
    def taux_remplissage(self):
        """Pourcentage de remplissage de l'entrepôt"""
        if self.capacite_max > 0:
            return (self.stock_actuel / self.capacite_max) * 100
        return 0
    
    @property
    def alerte_stock_bas(self):
        """Vérifie si le stock est en dessous du seuil d'alerte"""
        return self.stock_actuel < self.seuil_alerte


class Stock(models.Model):
    """Gestion du stock dans un entrepôt"""
    entrepot = models.ForeignKey(Entrepot, on_delete=models.CASCADE, related_name='stocks')
    type_culture = models.ForeignKey(TypeCulture, on_delete=models.CASCADE, related_name='stocks')
    quantite = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], help_text="Quantité en stock en kg")
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['entrepot', 'type_culture']
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        unique_together = ['entrepot', 'type_culture']
    
    def __str__(self):
        return f"{self.entrepot.nom} - {self.type_culture}: {self.quantite}kg"