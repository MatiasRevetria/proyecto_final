from django import forms
from .models import Receta, Comentario

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
