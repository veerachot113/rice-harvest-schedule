#accounts/permissions.py

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create groups and permissions for custom user roles'

    def handle(self, *args, **kwargs):
        farmer_group, created = Group.objects.get_or_create(name='farmer')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created group "farmer"'))
        else:
            self.stdout.write(self.style.WARNING('Group "farmer" already exists'))

        driver_group, created = Group.objects.get_or_create(name='driver')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created group "driver"'))
        else:
            self.stdout.write(self.style.WARNING('Group "driver" already exists'))

        self.stdout.write(self.style.SUCCESS('Successfully created groups and permissions'))

