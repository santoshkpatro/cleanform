import jwt
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from urllib.parse import urlencode
from smtplib import SMTPException


@shared_task
def send_registration_email(email):
    payload = {
        'email': email,
        'exp': timezone.now() + timezone.timedelta(minutes=10)
    }
    encoded_token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
    registration_url = settings.FRONTEND_BASE_URL + 'auth/register/?' + urlencode({'token': encoded_token})
    try:
        subject = 'Registration request'
        html_message = render_to_string('auth/registration_email.html', {'email': email, 'registration_url': registration_url})
        plain_message = strip_tags(html_message)
        from_email = settings.NO_REPLY_EMAIL
        to_email = email

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=[to_email],
            html_message=html_message,
            fail_silently=False
        )
    except SMTPException as e:
        print('Error')