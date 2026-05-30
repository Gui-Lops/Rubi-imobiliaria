from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistrationForm, ContatoForm
from .models import Property, PropertyImage

from .decorators import role_required


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Usuário ou senha incorretos.')
        return super().form_invalid(form)


def home(request):
    return render(request, 'loja/home.html')

def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
           
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            
            try:
                send_mail(
                    f'Novo contato: {subject}',
                    f'Nome: {name}\nEmail: {email}\nTelefone: {phone}\n\nMensagem:\n{message}',
                    email,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Mensagem enviada com sucesso! Em breve entraremos em contato.')
                return redirect('contato')
            except Exception as e:
                messages.error(request, 'Erro ao enviar mensagem. Tente novamente.')
    else:
        form = ContatoForm()
    
    return render(request, 'contato/contato.html', {'form': form})


def sobre(request):
    return render(request, 'loja/sobre.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            admin_code = form.cleaned_data.get('admin_code')
            if admin_code:
                user.is_staff = True
            user.email = form.cleaned_data.get('email')
            user.save()
            login(request, user)
            messages.success(request, 'Registro realizado com sucesso.')
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'loja/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'loja/profile.html')


@role_required('admin')
def admin_dashboard(request):
    return render(request, 'loja/admin_dashboard.html')
