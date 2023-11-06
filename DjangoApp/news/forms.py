from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomSignupForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'name', 'placeholder': 'Username'}),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Your Email'}),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'pass', 'placeholder': 'Password'}),
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 're_pass', 'placeholder': 'Repeat your password'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
