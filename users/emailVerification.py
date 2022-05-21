from django.core.mail import send_mail
import random
from django.conf import settings
from django.core.cache import cache

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
    patient = User.objects.get(email=email)
    patient.otp = otp
    patient.save()
    return True
