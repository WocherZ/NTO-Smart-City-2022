from .models import Patient, Doctor
from functools import wraps
from django.http import HttpResponseForbidden


def doctor_permission(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.session.get('role') == 2:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return decorator


def login_required(function):
    def decorator(request):
        if request.session.get('is_login'):
            return function(request)
        else:
            return HttpResponseForbidden()
    return decorator


def check_registration(login):
    user = Patient.objects.filter(login=login)
    if user.first():  # Нашёлся пациент
        return 1
    else:
        user = Doctor.objects.filter(login=login)
        if user.first():
            return 2
        else:
            return 0
