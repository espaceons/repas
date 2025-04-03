# ingredients/forms.py
from django import forms
from .models import Ingredient

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['nom', 'prix_unitaire', 'unite_mesure']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prix_unitaire': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'unite_mesure': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'nom': 'Nom de l\'ingrédient',
            'prix_unitaire': 'Prix unitaire (€)',
            'unite_mesure': 'Unité de mesure'
        }