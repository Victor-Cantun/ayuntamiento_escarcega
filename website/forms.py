from django import forms
from .models import (
    PostImage,
    accounting,
    document,
    gazette,
    director,
    dependence,
    carousel,
    council,
    Post,
)


class councilForm(forms.ModelForm):
    class Meta:
        model = council
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "firstlastname": forms.TextInput(attrs={"class": "form-control"}),
            "secondlastname": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "cellphone": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "director": forms.Select(attrs={"class": "form-control"}),
            "position": forms.Select(attrs={"class": "form-control"}),
            "profile_image": forms.FileInput(attrs={"class": "form-control"}),
        }


class directorForm(forms.ModelForm):
    class Meta:
        model = director
        fields = "__all__"


class dependenceForm(forms.ModelForm):
    class Meta:
        model = dependence
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "director": forms.Select(attrs={"class": "form-control"}),
        }


class carouselForm(forms.ModelForm):
    class Meta:
        model = carousel
        fields = "__all__"


class accountingForm(forms.ModelForm):
    class Meta:
        model = accounting
        fields = ["name", "dependence", "quarterly", "year", "document"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "dependence": forms.Select(attrs={"class": "form-control"}),
            "quarterly": forms.TextInput(attrs={"class": "form-control"}),
            "year": forms.TextInput(attrs={"class": "form-control"}),
            "document": forms.FileInput(attrs={"class": "form-control"}),
        }


class gazetteForm(forms.ModelForm):
    class Meta:
        model = gazette
        fields = "__all__"


class documentForm(forms.ModelForm):
    class Meta:
        model = document
        fields = "__all__"


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ["image", "caption"]
