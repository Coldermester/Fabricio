from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import models

# from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Car


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text=_("Obrigatório. Informe um email válido."),
        label=_("Email"),
    )

    password1 = forms.CharField(
        label=_("Senha"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_("Sua senha deve conter pelo menos 8 caracteres."),
    )

    password2 = forms.CharField(
        label=_("Confirmação da senha"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_("Repita a senha para confirmação."),
    )

    class Meta:
        User = get_user_model()
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": _("Nome de usuário"),
            "email": _("Email"),
        }
        help_texts = {
            "username": _(
                "Obrigatório. 150 caracteres ou menos. Letras, dígitos e @/./+/-/_ apenas."
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = get_user_model()


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["name", "brand"]
