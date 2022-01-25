from cProfile import label
from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label="Addresse Email", max_length=150)
    password = forms.CharField(label="Mot de Passe", widget=forms.PasswordInput())


class SignupForm(forms.Form):
    email = forms.EmailField(label="Addresse Email", max_length=150)
    username = forms.CharField(label="Pseudonyme", max_length=150)
    password = forms.CharField(label="Mot de Passe", widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        label="Confirmer le Mot de Passe", widget=forms.PasswordInput()
    )
