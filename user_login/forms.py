from django import forms

class New_user(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
        label='Usuario'
    )
    passwd = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control'}),
        label='Contraseña'
    )
    passwd2 = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña', 'class': 'form-control'}),
        label='Confirmar Contraseña'
    )

class Old_user(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
        label='Usuario'
    )
    passwd = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control'}),
        label='Contraseña'
    )
