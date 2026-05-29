from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Property


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ContactForm(forms.Form):
    SUBJECT_CHOICES = [
        ('', 'Selecione o assunto'),
        ('informacoes', 'Informações gerais'),
        ('agendamento', 'Agendamento de visita'),
        ('orcamento', 'Orçamento de imóvel'),
        ('outros', 'Outros'),
    ]

    name = forms.CharField(
        label='Nome Completo',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Seu nome completo',
            'class': 'input-field',
        })
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'seu@email.com',
            'class': 'input-field',
        })
    )
    phone = forms.CharField(
        label='Telefone',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '(11) 99999-9999',
            'class': 'input-field',
        })
    )
    subject = forms.ChoiceField(
        label='Assunto',
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={'class': 'input-field'})
    )
    message = forms.CharField(
        label='Mensagem',
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Conte-nos como podemos ajudá-lo...',
            'rows': 6,
            'class': 'input-field textarea-field',
        })
    )


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
