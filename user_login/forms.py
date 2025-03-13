from django import forms

class New_user(forms.Form):
    name = forms.CharField(label="Nombre de usuario",max_length=255)
    passwd = forms.CharField(label="Ingrese contrasena",max_length=255)