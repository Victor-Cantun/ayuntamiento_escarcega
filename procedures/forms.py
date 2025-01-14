from django import forms
from .models import citizen, request

class citizenForm(forms.ModelForm):
    class Meta:
        model:citizen
        fields="__all__"

class requestForm(forms.ModelForm):
    class Meta:
        model:request
        fields="__all__"