from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from PrisonerExpress.models import UserProfile

class PrisonerForm(forms.Form):
    prisoner_name = forms.CharField(label="Prisoner Name", max_length = 100)
    #Unfinished


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
