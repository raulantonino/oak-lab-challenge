from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Ej: ash_ketchum",
                "autocomplete": "username",
            }
        ),
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "Ingresa tu contraseña",
                "autocomplete": "new-password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "Repite tu contraseña",
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = (
            "Usa una contraseña segura con letras, números y símbolos."
        )
        self.fields["password2"].help_text = "Debe coincidir con la contraseña anterior."