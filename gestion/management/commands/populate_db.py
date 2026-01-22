from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from gestion.models import (
    Commune, Arrondissement, Producteur, Parcelle,
    TypeCulture, Recolte, Entrepot, Stock
)
from datetime import date, timedelta
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Remplit la base de données avec des données de test réalistes'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Début du peuplement de la base de données...'))
        
        # 1. CRÉER LES COMMUNES
        self.stdout.write('📍 Création des communes...')
        communes_data = [
            ('Cotonou', 'COT'),
            ('Porto-Novo', 'PN'),
            ('Parakou', 'PAR'),
            ('Abomey-Calavi', 'AC'),
            ('Djougou', 'DJO'),
        ]
        
        communes = {}
        for nom, code in communes_data:
            commune, created = Commune.objects.get_or_create(
                nom=nom,
                defaults={'code': code}
            )
            communes[nom] = commune
            if created:
                self.stdout.write(f'  ✅ {nom}')
        
        # 2. CRÉER LES ARRONDISSEMENTS
        self.stdout.write('🗺️  Création des arrondissements...')
        arrondissements_data = [
            ('Akpakpa', communes['Cotonou'], 'AKP'),
            ('Cadjehoun', communes['Cotonou'], 'CAD'),
            ('Godomey', communes['Abomey-Calavi'], 'GOD'),
            ('Vedoko', communes['Porto-Novo'], 'VED'),
            ('Ouando', communes['Porto-Novo'], 'OUA'),
            ('Banikanni', communes['Parakou'], 'BAN'),
        ]
        
        arrondissements = {}
        for nom, commune, code in arrondissements_data:
            arr, created = Arrondissement.objects.get_or_create(
                nom=nom,
                commune=commune,
                defaults={'code': code}
            )
            arrondissements[nom] = arr
            if created:
                self.stdout.write(f'  ✅ {nom} ({commune.nom})')
        
        # 3. CRÉER LES TYPES DE CULTURE
        self.stdout.write('🌾 Création des types de culture...')
        cultures_data = [
            ('MAIS', 'Culture principale de maïs'),
            ('SOJA', 'Culture de soja riche en protéines'),
            ('ANANAS', 'Culture d\'ananas pour l\'export'),
        ]
        
        cultures = {}
        for nom, description in cultures_data:
            culture, created = TypeCulture.objects.get_or_create(
                nom=nom,
                defaults={'description': description}
            )
            cultures[nom] = culture
            if created:
                self.stdout.write(f'  ✅ {culture.get_nom_display()}')
        
        # 4. CRÉER LES GROUPES (si pas déjà fait)
        self.stdout.write('👥 Vérification des groupes...')
        groupe_producteur, _ = Group.objects.get_or_create(name='Producteur')
        groupe_gestionnaire, _ = Group.objects.get_or_create(name='Gestionnaire')
        
        # 5. CRÉER DES PRODUCTEURS
        self.stdout.write('👨‍🌾 Création des producteurs...')
        producteurs_data = [
            ('Jean', 'Kouassi', 'jkouassi', '97123456', arrondissements['Akpakpa']),
            ('Marie', 'Dossou', 'mdossou', '97234567', arrondissements['Cadjehoun']),
            ('Paul', 'Agbodjan', 'pagbodjan', '97345678', arrondissements['Godomey']),
            ('Esther', 'Houngbo', 'ehoungbo', '97456789', arrondissements['Vedoko']),
            ('Joseph', 'Kpade', 'jkpade', '97567890', arrondissements['Banikanni']),
        ]
        
        producteurs = []
        for prenom, nom, username, tel, arr in producteurs_data:
            # Créer l'utilisateur
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': prenom,
                    'last_name': nom,
                    'email': f'{username}@agritech.bj'
                }
            )
            if created:
                user.set_password('producteur123')
                user.save()
                user.groups.add(groupe_producteur)
            
            # Créer le producteur
            producteur, created = Producteur.objects.get_or_create(
                user=user,
                defaults={
                    'telephone': tel,
                    'arrondissement': arr,
                    'actif': True
                }
            )
            producteurs.append(producteur)
            if created:
                self.stdout.write(f'  ✅ {prenom} {nom}')
        
        # 6. CRÉER UN SUPERUSER (ADMIN)
        self.stdout.write('👑 Création du superuser (Admin)...')
        superuser, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'TIDJANI',
                'last_name': 'Mohamed Amine',
                'email': 'admin@agritech.bj',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            superuser.set_password('admin@2026')
            superuser.save()
            self.stdout.write('  ✅ Admin (TIDJANI Mohamed Amine)')
        
        # 7. CRÉER UN GESTIONNAIRE
        self.stdout.write('👨‍💼 Création du gestionnaire...')
        user_gest, created = User.objects.get_or_create(
            username='gestionnaire1',
            defaults={
                'first_name': 'Sylvie',
                'last_name': 'Mensah',
                'email': 'gestionnaire@agritech.bj'
            }
        )
        if created:
            user_gest.set_password('gestionnaire123')
            user_gest.save()
            user_gest.groups.add(groupe_gestionnaire)
            self.stdout.write('  ✅ Sylvie Mensah')
        
        # 7. CRÉER DES PARCELLES
        self.stdout.write('🗺️  Création des parcelles...')
        parcelles = []
        parcelles_data = [
            (producteurs[0], 'Parcelle Nord', arrondissements['Akpakpa'], 2.5, 6.3703, 2.3912),
            (producteurs[0], 'Parcelle Sud', arrondissements['Akpakpa'], 1.8, 6.3650, 2.3850),
            (producteurs[1], 'Champ Central', arrondissements['Cadjehoun'], 3.2, 6.3580, 2.4020),
            (producteurs[2], 'Grande Parcelle', arrondissements['Godomey'], 4.5, 6.4120, 2.3330),
            (producteurs[3], 'Terrain Est', arrondissements['Vedoko'], 2.0, 6.4970, 2.6290),
            (producteurs[4], 'Zone Agricole', arrondissements['Banikanni'], 5.0, 9.3370, 2.6300),
        ]
        
        for prod, nom, arr, superficie, lat, lon in parcelles_data:
            parcelle, created = Parcelle.objects.get_or_create(
                producteur=prod,
                nom=nom,
                defaults={
                    'arrondissement': arr,
                    'superficie': Decimal(str(superficie)),
                    'latitude': Decimal(str(lat)),
                    'longitude': Decimal(str(lon))
                }
            )
            parcelles.append(parcelle)
            if created:
                self.stdout.write(f'  ✅ {nom} ({prod.user.get_full_name()})')
        
        # 8. CRÉER DES RÉCOLTES
        self.stdout.write('🌾 Création des récoltes...')
        recoltes_count = 0
        cultures_list = [cultures['MAIS'], cultures['SOJA'], cultures['ANANAS']]
        
        for parcelle in parcelles:
            # Créer 3-5 récoltes par parcelle
            nb_recoltes = random.randint(3, 5)
            for i in range(nb_recoltes):
                culture = random.choice(cultures_list)
                quantite = random.randint(300, 1500)
                date_recolte = date.today() - timedelta(days=random.randint(1, 180))
                
                Recolte.objects.get_or_create(
                    parcelle=parcelle,
                    type_culture=culture,
                    date_recolte=date_recolte,
                    defaults={'quantite': Decimal(str(quantite))}
                )
                recoltes_count += 1
        
        self.stdout.write(f'  ✅ {recoltes_count} récoltes créées')
        
        # 9. CRÉER DES ENTREPÔTS
        self.stdout.write('🏭 Création des entrepôts...')
        entrepots_data = [
            ('Entrepôt Central Cotonou', arrondissements['Akpakpa'], 15000, 3000),
            ('Dépôt Porto-Novo', arrondissements['Vedoko'], 10000, 2000),
            ('Stockage Parakou', arrondissements['Banikanni'], 12000, 2500),
        ]
        
        entrepots = []
        for nom, arr, capacite, seuil in entrepots_data:
            entrepot, created = Entrepot.objects.get_or_create(
                nom=nom,
                defaults={
                    'arrondissement': arr,
                    'capacite_max': Decimal(str(capacite)),
                    'seuil_alerte': Decimal(str(seuil)),
                    'gestionnaire': user_gest
                }
            )
            entrepots.append(entrepot)
            if created:
                self.stdout.write(f'  ✅ {nom}')
        
        # 10. CRÉER DES STOCKS
        self.stdout.write('📦 Création des stocks...')
        stocks_data = [
            (entrepots[0], cultures['MAIS'], 8500),
            (entrepots[0], cultures['SOJA'], 1800),  # En dessous du seuil = ALERTE
            (entrepots[0], cultures['ANANAS'], 4200),
            (entrepots[1], cultures['MAIS'], 6000),
            (entrepots[1], cultures['SOJA'], 3500),
            (entrepots[2], cultures['MAIS'], 7500),
            (entrepots[2], cultures['ANANAS'], 2800),
        ]
        
        for entrepot, culture, quantite in stocks_data:
            Stock.objects.get_or_create(
                entrepot=entrepot,
                type_culture=culture,
                defaults={'quantite': Decimal(str(quantite))}
            )
        
        self.stdout.write(f'  ✅ {len(stocks_data)} stocks créés')
        
        # RÉSUMÉ FINAL
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✅ BASE DE DONNÉES PEUPLÉE AVEC SUCCÈS !'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.WARNING('\n📊 RÉSUMÉ DES DONNÉES CRÉÉES :'))
        self.stdout.write(f'   • {Commune.objects.count()} communes')
        self.stdout.write(f'   • {Arrondissement.objects.count()} arrondissements')
        self.stdout.write(f'   • {TypeCulture.objects.count()} types de culture')
        self.stdout.write(f'   • {Producteur.objects.count()} producteurs')
        self.stdout.write(f'   • {Parcelle.objects.count()} parcelles')
        self.stdout.write(f'   • {Recolte.objects.count()} récoltes')
        self.stdout.write(f'   • {Entrepot.objects.count()} entrepôts')
        self.stdout.write(f'   • {Stock.objects.count()} stocks')
        
        self.stdout.write(self.style.WARNING('\n🔐 COMPTES CRÉÉS :'))
        self.stdout.write('   SUPERUSER (ADMIN) :')
        self.stdout.write('      • admin / admin@2026')
        self.stdout.write('   PRODUCTEURS :')
        for prod in producteurs:
            self.stdout.write(f'      • {prod.user.username} / producteur123')
        self.stdout.write('   GESTIONNAIRE :')
        self.stdout.write('      • gestionnaire1 / gestionnaire123')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Vous pouvez maintenant vous connecter !'))