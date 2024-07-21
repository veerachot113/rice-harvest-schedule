#Accounts/permissions.py

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create groups and permissions for custom user roles'

    def handle(self, *args, **kwargs):
        # Create or get the 'farmer' group
        farmer_group, created = Group.objects.get_or_create(name='farmer')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created group "farmer"'))
        else:
            self.stdout.write(self.style.WARNING('Group "farmer" already exists'))

        # Create or get the 'driver' group
        driver_group, created = Group.objects.get_or_create(name='driver')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created group "driver"'))
        else:
            self.stdout.write(self.style.WARNING('Group "driver" already exists'))

        # Assign permissions to groups (if needed)
        # For example, assigning all permissions for a specific model to the 'driver' group
        # content_type = ContentType.objects.get_for_model(YourModel)
        # permissions = Permission.objects.filter(content_type=content_type)
        # driver_group.permissions.set(permissions)

        # You can assign specific permissions as needed

        # Output success message
        self.stdout.write(self.style.SUCCESS('Successfully created groups and permissions'))
