# gestion/management/commands/setup_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Configure les groupes et permissions pour AgriTech-Bénin'

    def handle(self, *args, **kwargs):
        # Créer le groupe PRODUCTEUR
        producteur_group, created = Group.objects.get_or_create(name='Producteur')
        
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Groupe "Producteur" créé'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Groupe "Producteur" existe déjà'))
        
        # Permissions pour les Producteurs (lecture seule de leurs données)
        producteur_permissions_codenames = [
            'view_recolte',
            'add_recolte',
            'view_parcelle',
            'view_producteur',
            'change_producteur',
        ]
        
        for codename in producteur_permissions_codenames:
            try:
                permission = Permission.objects.get(codename=codename)
                producteur_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'⚠️ Permission "{codename}" non trouvée'))
        
        self.stdout.write(self.style.SUCCESS('✅ Permissions "Producteur" configurées'))
        
        # Créer le groupe GESTIONNAIRE
        gestionnaire_group, created = Group.objects.get_or_create(name='Gestionnaire')
        
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Groupe "Gestionnaire" créé'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Groupe "Gestionnaire" existe déjà'))
        
        # Permissions pour les Gestionnaires (TOUT sur l'app gestion)
        gestionnaire_permissions = Permission.objects.filter(
            content_type__app_label='gestion'
        )
        
        for permission in gestionnaire_permissions:
            gestionnaire_group.permissions.add(permission)
        
        self.stdout.write(self.style.SUCCESS('✅ Permissions "Gestionnaire" configurées'))
        self.stdout.write(self.style.SUCCESS(f'   Total: {gestionnaire_permissions.count()} permissions'))
        
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('🎉 Configuration terminée !'))
        self.stdout.write(self.style.WARNING(''))
        self.stdout.write(self.style.WARNING('📝 PROCHAINES ÉTAPES :'))
        self.stdout.write(self.style.WARNING('1. Allez sur http://127.0.0.1:8000/admin/'))
        self.stdout.write(self.style.WARNING('2. Cliquez sur "Utilisateurs"'))
        self.stdout.write(self.style.WARNING('3. Sélectionnez un utilisateur'))
        self.stdout.write(self.style.WARNING('4. Dans la section "Groupes", ajoutez "Producteur" ou "Gestionnaire"'))
        self.stdout.write(self.style.WARNING('5. Sauvegardez'))