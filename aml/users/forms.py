from django import forms
from django.contrib.auth import authenticate
from users.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label="Addresse Email", max_length=150)
    password = forms.CharField(label="Mot de Passe", widget=forms.PasswordInput())

    def get_user(self, request):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]

        return authenticate(request, email=email, password=password)


class SignupForm(forms.Form):
    email = forms.EmailField(label="Addresse Email", max_length=150)
    username = forms.CharField(label="Pseudonyme", max_length=150)
    password = forms.CharField(label="Mot de Passe", widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        label="Confirmer le Mot de Passe", widget=forms.PasswordInput()
    )

    def get_user(self, request):
        email = self.cleaned_data["email"]
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]

        if password != confirm_password:
            print("Incorrect confirmation")
            return None

        if User.objects.filter(email=email).exists():
            print("Email deja existante")
            return None

        try:
            user = User.objects.create_user(username, email, password)
        except Exception as error:
            print(error)
            print("Impossible de creer")
            return None

        user.save()

        return authenticate(request, email=email, password=password)
