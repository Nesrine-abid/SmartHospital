from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache

from .models import Employee

def send_email_for_employee(email):
    if cache.get(email):
        return False
    subject = "your Smart hospital verification account email"
    message = f'Your Email is now verified by the admin you can log in '
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    return True