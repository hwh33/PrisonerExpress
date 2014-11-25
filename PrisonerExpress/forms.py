from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from PrisonerExpress.models import UserProfile

class PrisonerForm(forms.Form):
    prisoner_name = forms.CharField(label="Prisoner Name", max_length = 100)
    #Unfinished



