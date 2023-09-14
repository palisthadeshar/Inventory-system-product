from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(user_email,reset_password_url, otp):
    subject = "Your OTP Code"
    message = f"Your otp code is {otp}. Go to the link {reset_password_url} to reset your password."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    
    
    send_mail(subject, message, from_email, recipient_list)