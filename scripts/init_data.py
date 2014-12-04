from django.contrib.auth.models import Group 
from PrisonerExpress.models import Letter
from django.contrib.auth.models import Permission

def init():
    gAdmins = Group(name='Admins')
    gAdmins.save()
    gVolunteer = Group(name='Volunteers')
    gVolunteer.save()
    permission = Permission.objects.get(codename='can_upload_letter')
    gVolunteer.permissions.add(permission)
    permission = Permission.objects.get(codename='can_translate_letter')
    gVolunteer.permissions.add(permission)


