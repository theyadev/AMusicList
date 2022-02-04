from django import forms
from django.contrib.auth import authenticate
from users.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label="Addresse Email", max_length=150, label_suffix="")
    password = forms.CharField(
        label="Mot de passe", widget=forms.PasswordInput(), label_suffix=""
    )

    def get_user(self, request):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]

        return authenticate(request, email=email, password=password)


class SignupForm(forms.Form):
    email = forms.EmailField(label="Addresse Email", max_length=150, label_suffix="")
    username = forms.CharField(label="Pseudonyme", max_length=150, label_suffix="")
    password = forms.CharField(
        label="Mot de passe", widget=forms.PasswordInput(), label_suffix=""
    )
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


class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        help_texts = {
            "username": None,
        }
        fields = ["username", "email"]
class SettingsPasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Ancien mot de passe", widget=forms.PasswordInput(), label_suffix=""
    )
    password = forms.CharField(
        label="Nouveau mot de passe", widget=forms.PasswordInput(), label_suffix=""
    )
    confirm_password = forms.CharField(
        label="Confirmer le mot de passe", widget=forms.PasswordInput()
    )

    def is_valid(self, user) -> bool:
        if not super().is_valid():
            return False

        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            return False
        
        if not user.check_password(self.cleaned_data['old_password']):
            return False

        return True

    def save(self, user):
        user.set_password(self.cleaned_data['password'])
        user.save()
        
        return user
