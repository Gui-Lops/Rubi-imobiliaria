from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Property


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


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
