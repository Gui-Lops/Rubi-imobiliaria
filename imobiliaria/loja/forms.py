from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    admin_code = forms.CharField(required=False, help_text='Preencha se for registro de admin', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'admin_code')

    def clean_admin_code(self):
        code = self.cleaned_data.get('admin_code')
        if code and code != settings.ADMIN_REGISTRATION_CODE:
            raise forms.ValidationError('Código de admin inválido')
        return code


class ContatoForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Nome Completo')
    email = forms.EmailField(required=True, label='E-mail')
    phone = forms.CharField(max_length=20, required=True, label='Telefone')
    subject = forms.CharField(max_length=200, required=True, label='Assunto')
    message = forms.CharField(widget=forms.Textarea, required=True, label='Mensagem')