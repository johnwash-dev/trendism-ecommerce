import secrets
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    return ''.join(secrets.choice("0123456789") for _ in range(6))

def send_email_otp(email, otp):
    send_mail(
        subject = 'OTP verification code',
        message = f'Your OTP is {otp}. it is valid for 5 minutes',
        from_email = settings.DEFAULT_FROM_EMAIL,
        recipient_list = [email],
        fail_silently = False
    )

