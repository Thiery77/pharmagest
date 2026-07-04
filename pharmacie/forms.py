from django import forms
from .models import Medicament

class MedicamentForm(forms.ModelForm):
    class Meta:
        model = Medicament
        fields = '__all__'  # Tous les champs du modèle
        widgets = {
            'date_peremption': forms.DateInput(attrs={'type': 'date'}),
        }