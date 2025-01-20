import random
from string import hexdigits
from allauth.account.forms import SignupForm
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код активации',
            message=f'Код активации аккаунта: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user

    def save_resp_author(self, request):
        user = super().save(request)
        resp_authors = Group.objects.get(name="resp_authors")
        user.groups.add(resp_authors)
        return user
