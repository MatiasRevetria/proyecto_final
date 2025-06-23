from django import forms
from django.forms import modelformset_factory
from .models import Receta, Comentario, RecetaIngrediente, Ingrediente,Valoracion, DIFICULTADES, CATEGORIAS, VALORACION

class RecetaNueva(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['title', 'description', 'coccion', 'image', 'categoria', 'dificultad']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Título de la receta', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Descripción detallada', 'class': 'form-control'}),
            'coccion': forms.NumberInput(attrs={'placeholder': 'Minutos de cocción', 'class': 'form-control'}),
            'categoria': forms.Select(choices=CATEGORIAS, attrs={'class':'form.select'}),
            'dificultad': forms.Select(choices=DIFICULTADES, attrs={'class': 'form-select'}),
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
    fields=('nombre', 'cantidad', 'unidad'),
    extra=3,
    can_delete=True
)

class ValorarRecetaForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['puntaje']
        widgets = {
            'puntaje': forms.RadioSelect(choices= VALORACION)
        }