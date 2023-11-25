from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ArticleComment, UserProfile

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


class NewCommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control mr-3', 'placeholder': 'Add comment'}),
    )
    class Meta:
        model = ArticleComment
        fields = ['content']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']

    profile_image = forms.ImageField(widget=forms.ClearableFileInput(), required=False)
