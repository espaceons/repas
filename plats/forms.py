
from django import forms
from .models import Plat
from recettes.models import Recette

class PlatForm(forms.ModelForm):
    class Meta:
        model = Plat
        fields = ['recette', 'type_plat', 'date_preparation', 'portions']
        widgets = {
            'recette': forms.Select(attrs={'class': 'form-control'}),
            'date_preparation': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recette'].queryset = Recette.objects.all()