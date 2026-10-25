from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# NOTE: ProfileUpdateForm removed — it incorrectly referenced the raw 'password'
# hash field via ModelForm, which is not safe or functional. Password changes
# are handled by Django's built-in PasswordChangeForm in users/views.py.
