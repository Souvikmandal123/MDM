import random
from django.core.mail import send_mail
from django.conf import settings
from .models import OTP

def generate_otp():
    return str(random.randint(100000, 999999))

def create_and_send_otp(user, purpose):
    code = generate_otp()
    otp = OTP.objects.create(user=user, code=code, purpose=purpose)
    print("otp : {}".format(otp))
    send_mail(
        subject=f"Your {purpose} OTP",
        message=f"Your OTP is {code}. It expires in 10 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )
    return otp
