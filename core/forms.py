from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class ExpressaoForm(forms.Form):
    expressao = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite uma expressão',
            'autocomplete': 'off'
        }),
        max_length=255
    )

class CadastroForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput,
        help_text="A senha deve conter pelo menos 5 caracteres."
    )
    confirmar_senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'senha', 'confirmar_senha']
        labels = {
            'username': 'Usuário',
            'first_name': 'Primeiro nome',
            'email': 'Email',
            'senha': 'Senha',
            'confirmar_senha': 'Confirmar senha',
        }
        help_texts = {
            'username': '',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Será utilizado para o login'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(regex, email):
            raise ValidationError('Insira um e-mail válido.')
        return email

    def clean_senha(self):
        senha = self.cleaned_data.get('senha')
        if len(senha) < 5:
            raise ValidationError("A senha deve conter pelo menos 5 caracteres.")
        return senha

    def clean_confirmar_senha(self):
        senha = self.cleaned_data.get('senha')
        confirmar = self.cleaned_data.get('confirmar_senha')

        if senha and confirmar and senha != confirmar:
            raise ValidationError("As senhas não coincidem.")
        return confirmar