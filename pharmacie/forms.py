from django import forms
from .models import Medicament, Fournisseur

class MedicamentForm(forms.ModelForm):
    class Meta:
        model = Medicament
        fields = '__all__'

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = '__all__'