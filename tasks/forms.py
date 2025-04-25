from django import forms

from .models import *


class RecetaNueva(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Titulo','label':''}),max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description','label':''}),max_length=255)
    coccion = forms.IntegerField()