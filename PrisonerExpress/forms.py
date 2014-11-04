from django import forms

class PrisonerForm(forms.Form):
    prisoner_name = forms.CharField(label="Prisoner Name", max_length = 100)
