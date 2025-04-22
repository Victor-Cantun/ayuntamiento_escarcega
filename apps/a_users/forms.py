from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from allauth.account.forms import LoginForm


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "displayname", "info"]
        widgets = {
            "image": forms.FileInput(
                attrs={
                    "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
                }
            ),
            "displayname": forms.TextInput(
                attrs={
                    "placeholder": "Agrega tu nombre",
                    "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
            "info": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Agrega alguna información sobre tí",
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-2",
                }
            ),
        }


class CustomLoginForm(LoginForm):
    username = forms.CharField(
        label="Correo electrónico o Nombre de Usuario",
        widget=forms.TextInput(attrs={"placeholder": "Correo o Usuario"}),
    )
