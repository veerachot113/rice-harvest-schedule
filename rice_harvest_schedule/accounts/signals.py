# # accounts/signals.py

# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from django.contrib.auth.models import Group

# @receiver(post_migrate)
# def create_user_roles(sender, **kwargs):
#     if sender.name == 'accounts':
#         farmer_group, created = Group.objects.get_or_create(name='farmer')
#         if created:
#             print('Successfully created group "farmer"')
#         else:
#             print('Group "farmer" already exists')

#         driver_group, created = Group.objects.get_or_create(name='driver')
#         if created:
#             print('Successfully created group "driver"')
#         else:
#             print('Group "driver" already exists')
