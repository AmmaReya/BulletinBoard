from bulletinboard.models import User, Author
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'account/invalid_code.html')
        return redirect('account_login')


@login_required
def profile(request):
    is_not_author = not request.user.groups.filter(name="authors").exists()
    return render(request, 'profile.html', {'is_not_author': is_not_author})


@login_required
def be_author(request):
    user = request.user
    group = get_object_or_404(Group, name="authors")
    if not user.groups.filter(name='group.name').exists():
        user.groups.add(group)
    if not Author.objects.filter(author=user).exists():
        Author.objects.create(author=user)
    return redirect("profile")
