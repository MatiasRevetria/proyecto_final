from django import forms

class New_user(forms.Form):
    name = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'placeholder': 'Username'}),label='')
    passwd = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Password','type':'password'}),max_length=255,label='')
    passwd2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Confirm Password','type': 'password'}),max_length=255,label='')

class Old_user(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}),max_length=255,label='')
    passwd = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Password','type':'password'}),max_length=255,label='')

