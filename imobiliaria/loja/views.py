from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .forms import RegistrationForm
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
