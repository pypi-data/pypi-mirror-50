from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail

my_email = 'kathurimakimathi415@gmail.com'


@shared_task
def mailer(subject, message, recipient_list, from_who=my_email):
    send_mail(subject, message, recipient_list, from_who)
