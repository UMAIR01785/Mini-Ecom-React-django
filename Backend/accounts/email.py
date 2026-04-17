from django.utils.encoding import force_bytes
from .tokens import activate_account
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def Activate_email(user):
    token=activate_account.make_token(user)
    link=f"http://127.0.0.1:8000/api/account/activate/{user.id}/{token}/"
    subject="Activate the account"
    
    body=f" Hy {user.first_name}-{user.last_name} please click the link to active the account{link}"
    email=EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )
    email.send()