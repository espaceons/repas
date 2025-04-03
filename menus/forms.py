# menu/forms.py
from django import forms
from .models import Menu, Plat, MenuPlat

class MenuPlatsForm(forms.ModelForm):
    plats = forms.ModelMultipleChoiceField(
        queryset=Plat.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Menu
        fields = ['nom', 'date_service', 'plats']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['plats'].initial = self.instance.plats.all()

    def save(self, commit=True):
        menu = super().save(commit=False)
        if commit:
            menu.save()
        plats = self.cleaned_data['plats']
        MenuPlat.objects.filter(menu=menu).delete()  # Supprime les plats existants
        for order, plat in enumerate(plats, start=1):
            MenuPlat.objects.create(menu=menu, plat=plat, ordre=order)
        return menu