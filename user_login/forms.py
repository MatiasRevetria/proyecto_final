from django import forms

class New_user(forms.Form):
    name = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'placeholder': 'User'}),label='')
    passwd = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Password'}),max_length=255,label='')