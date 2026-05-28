from django.contrib.auth.decorators import user_passes_test


def role_required(role='admin'):
    """Decorator factory: role='admin' checks user.is_staff; role='super' checks is_superuser."""
    def check(user):
        if not user.is_authenticated:
            return False
        if role == 'admin':
            return user.is_staff
        if role == 'super':
            return user.is_superuser
        return False

    return user_passes_test(check, login_url='/login/')
