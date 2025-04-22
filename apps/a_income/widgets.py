from django_select2 import forms as s2forms
from django_select2.forms import ModelSelect2Widget
from .models import Category

class CategoryWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]
    attrs = {
        "data-minimum-input-length": 0,
        "data-placeholder": "Selecciona una opción",
        "data-close-on-select": "false",
        "autocomplete": "on",
    }

    def get_queryset(self):
        return Category.objects.all()
    
class ConceptWidget(ModelSelect2Widget):
    search_fields = [
        'name__icontains', 
    ]

    dependent_fields = {'category': 'category'}


    def filter_queryset(self, term, queryset=None, **dependent_fields):

        assert queryset is not None
        caategory_id = dependent_fields.get('category', None)
        if caategory_id:
            queryset = queryset.filter(caategory_id=caategory_id)
        if term:
            queryset = queryset.filter(name__icontains=term)
        return queryset