from django import forms
from .models import Produtor, Terreno, Talhao
from django.forms import DateInput

class ProdutorForm(forms.ModelForm):
    class Meta:
        model = Produtor
        exclude = ['coordenador', 'cidade']
        widgets = {
            'validade_caf': DateInput(attrs={'type': 'date'})
        }
        labels = {
            'validade_caf': 'Validade do CAF',
        }

class TerrenoForm(forms.ModelForm):
    class Meta:
        model = Terreno
        exclude = ['produtor', 'cidade']

class TalhaoForm(forms.ModelForm):
    class Meta:
        model = Talhao
        exclude = ['terreno', 'cidade']
        widgets = {
            'validade_caf': DateInput(attrs={'type': 'date'}),
            'data_plantio': DateInput(attrs={'type': 'date'}),
            'data_certificacao': DateInput(attrs={'type': 'date'})
        }
        labels = {
            'validade_caf': 'Validade do CAF',
            'data_plantio': 'Data de Plantio',
            'data_certificacao': 'Data da Certificação'
        }