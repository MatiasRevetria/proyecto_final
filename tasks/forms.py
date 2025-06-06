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
    fields=('nombre', 'unidad', 'cantidad'),
    extra=3,  # cantidad de formularios vacíos por defecto
    widgets={
        'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Harina'}),
        'unidad': forms.TextInput(attrs={'placeholder': 'Ej: gramos'}),
        'cantidad': forms.NumberInput(attrs={'placeholder': 'Ej: 100'}),
    }
)
