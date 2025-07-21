from django import forms
from .models import Produtor
from django.forms import DateInput

class ProdutorForm(forms.ModelForm):
    class Meta:
        model = Produtor
        exclude = ['coordenador', 'estado', 'cidade']
        widgets = {
            'validade_caf': DateInput(attrs={'type': 'date'})
        }
