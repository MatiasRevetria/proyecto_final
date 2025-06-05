from django import forms
from django.forms import modelformset_factory
from .models import Receta, Comentario, RecetaIngrediente, Ingrediente

class RecetaNueva(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['title', 'description', 'coccion', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Título'}),
            'description': forms.Textarea(attrs={'placeholder': 'Descripción'}),
            'coccion': forms.NumberInput(attrs={'placeholder': 'Minutos'}),
        }

class ComentarReceta(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['txt']
        widgets = {
            'txt': forms.Textarea(attrs={
                'placeholder': 'Escribí un comentario...',
                'rows': 3,
                'cols': 40
            })
        }

RecetaIngredienteFormSet = modelformset_factory(
    RecetaIngrediente,
    fields=('ingrediente',),
    extra = 4,
)
