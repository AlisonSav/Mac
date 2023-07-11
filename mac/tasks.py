from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail


@shared_task
def add(x, y):
    return x + y


@shared_task
def send_remind(subject, email, message):
    mail_sent = send_mail(subject,
                          message,
                          settings.NOREPLY_EMAIL,
                          [email],
                          fail_silently=False,
                          )
    return mail_sent
