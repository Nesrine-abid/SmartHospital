from django.core.mail import send_mail
import random
from django.conf import settings
from django.core.cache import cache

from EmployeeApp.models import Employee
from .models import User, Patient


def send_otp_via_email(email):
    if cache.get(email):
        return False
    subject = "your Smart hospital verification account email"
    otp = random.randint(1000, 9999)
    cache.set(email, otp, timeout=60)
    message = f'Your code verification is {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    patient = Patient.objects.get(email=email)
    patient.otp = otp
    patient.save()
    return True


def send_confirmation_email(email):
    if cache.get(email):
        return False
    subject = "your Smart hospital confirmation account email"
    message = f'Your account is now confirmed you may acces your account on Smart Hospital app'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    employee = Employee.objects.get(email=email)
    employee.save()
    return True
