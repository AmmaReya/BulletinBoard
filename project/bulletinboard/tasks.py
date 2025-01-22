from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, User
import datetime
from django.conf import settings


@shared_task
def send_mail_monday_8am():
    now = datetime.datetime.now()
    posts = Post.objects.filter(post_time_in__gte=now - datetime.timedelta(days=7))
    users = set(User.objects.values_list('email', flat=True))
    html_content = render_to_string(
        'new_post_mail.html',
        {'link': settings.SITE_URL,
         'posts': posts})
    msg = EmailMultiAlternatives(
        subject='Объявления за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=users)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

