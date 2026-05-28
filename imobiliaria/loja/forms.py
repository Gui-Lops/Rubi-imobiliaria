from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Property


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

<<<<<<< HEAD
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
=======

class MultiImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class PropertyForm(forms.ModelForm):
    images = forms.FileField(
        required=False,
        widget=MultiImageInput(attrs={'multiple': True}),
        label='Imagens do imóvel',
        help_text='Envie várias imagens para o imóvel, separadas por upload múltiplo.'
    )

    class Meta:
        model = Property
        fields = ('title', 'location', 'price', 'property_type', 'description', 'is_published')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'property_type': forms.Select(),
        }
>>>>>>> b1a07c178218884a3c102a9574a2a30148a2e186
