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