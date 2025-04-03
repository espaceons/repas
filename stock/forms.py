
from django import forms
from .models import Stock

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['quantite', 'seuil_alerte']
        widgets = {
            'quantite': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'seuil_alerte': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        quantite = cleaned_data.get('quantite')
        seuil_alerte = cleaned_data.get('seuil_alerte')
        
        if quantite is not None and quantite < 0:
            self.add_error('quantite', "La quantité ne peut pas être négative")
        
        if seuil_alerte is not None and seuil_alerte < 0:
            self.add_error('seuil_alerte', "Le seuil d'alerte ne peut pas être négatif")
        
        return cleaned_data