from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .forms import ContactForm, RegistrationForm, PropertyForm
from .models import Property, PropertyImage
from .decorators import role_required


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return reverse('admin_dashboard')
        return reverse('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Usuário ou senha incorretos.')
        return super().form_invalid(form)


def home(request):
    return render(request, 'loja/home.html')


def contato(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Sua mensagem foi enviada com sucesso. Em breve entraremos em contato.')
            return redirect('contato')
    else:
        form = ContactForm()

    return render(request, 'loja/contato.html', {'contact_form': form})


def sobre(request):
    return render(request, 'loja/sobre.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()
            login(request, user)
            messages.success(request, 'Registro realizado com sucesso.')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'loja/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'loja/profile.html')


@role_required('admin')
def admin_dashboard(request):
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_properties = Property.objects.count()
    published_properties = Property.objects.filter(is_published=True).count()

    return render(request, 'loja/admin_dashboard.html', {
        'total_users': total_users,
        'active_users': active_users,
        'total_properties': total_properties,
        'published_properties': published_properties,
    })


@role_required('admin')
def admin_users(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        target_user = get_object_or_404(User, pk=user_id)

        if target_user == request.user:
            messages.error(request, 'Você não pode alterar seu próprio usuário aqui.')
            return redirect('admin_users')

        if action == 'toggle_staff':
            target_user.is_staff = not target_user.is_staff
            target_user.save()
            messages.success(request, 'Permissão de administrador atualizada.')
        elif action == 'toggle_active':
            target_user.is_active = not target_user.is_active
            target_user.save()
            messages.success(request, 'Status de usuário atualizado.')
        elif action == 'delete_user':
            target_user.delete()
            messages.success(request, 'Usuário removido com sucesso.')
        else:
            messages.error(request, 'Ação inválida.')

        return redirect('admin_users')

    users = User.objects.order_by('-is_staff', 'username')
    return render(request, 'loja/admin_users.html', {'users': users})


@role_required('admin')
def admin_properties(request):
    properties = Property.objects.order_by('-created_at')
    return render(request, 'loja/admin_properties.html', {'properties': properties})


@role_required('admin')
def admin_property_form(request, pk=None):
    property_instance = get_object_or_404(Property, pk=pk) if pk else None
    form = PropertyForm(request.POST or None, request.FILES or None, instance=property_instance)

    if request.method == 'POST' and form.is_valid():
        property_obj = form.save()

        uploaded_images = request.FILES.getlist('images')
        for image_file in uploaded_images:
            PropertyImage.objects.create(property=property_obj, image=image_file)

        messages.success(request, 'Imóvel salvo com sucesso.')
        return redirect('admin_properties')

    return render(request, 'loja/property_form.html', {
        'form': form,
        'property_instance': property_instance,
    })


def property_detail(request, pk):
    property_instance = get_object_or_404(Property, pk=pk)
    return render(request, 'loja/property_detail.html', {
        'property': property_instance,
    })


@role_required('admin')
def admin_property_delete(request, pk):
    property_instance = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property_instance.delete()
        messages.success(request, 'Imóvel removido com sucesso.')
    return redirect('admin_properties')


def logout_view(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('home')
