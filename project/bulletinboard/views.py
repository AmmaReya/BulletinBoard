from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .filters import PostFilter
from .models import Post, Response

from .forms import PostForm, ResponseForm
from django.shortcuts import redirect, render


class PostList(ListView):
    model = Post
    ordering = 'post_time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = 'post_time_in'
    template_name = 'post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('bulletinboard.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        new_post = form.save(commit=False)
        if self.request.method == 'POST':
            new_post.author = self.request.user.author
        new_post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostUpdate(PermissionRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('bulletinboard.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('bulletinboard.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('my_posts')


@login_required
def my_posts(request):
    user = request.user
    context = {'posts': Post.objects.filter(author__author__username=user)}
    return render(request, 'my_posts.html', context)


@login_required
def manage_responses(request):
    user = request.user
    posts = Post.objects.filter(author__author__username=user)
    selected_post = request.GET.get('post')
    if selected_post:
        responses = Response.objects.filter(post__pk=selected_post)
    else:
        responses = Response.objects.filter(post__in=posts)
    return render(request, 'resp_manage.html', {'responses': responses, 'posts': posts})


class ResponseCreate(LoginRequiredMixin, CreateView):
    permission_required = ('bulletinboard.add_response',)
    form_class = ResponseForm
    model = Response
    template_name = 'resp_edit.html'
    success_url = '/posts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        response = form.save(commit=False)
        response.resp_author = self.request.user
        response.post_id = self.kwargs['pk']
        response.save()
        send_mail(
            subject=f'Уведомление о новом отклике',
            message=f'{response.post.author}, вам оставили новый отклик: {response.text}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[response.post.author.author.email],
        )
        return super().form_valid(form)


class ResponseUpdate(PermissionRequiredMixin, UpdateView):
    raise_exception = True
    permission_required = ('bulletinboard.change_response',)
    form_class = ResponseForm
    model = Response
    template_name = 'resp_edit.html'
    success_url = '/posts/resp_manage/my_responses/'


class ResponseDeleteAuthor(PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('bulletinboard.delete_response',)
    model = Response
    template_name = 'resp_delete.html'
    success_url = '/posts/resp_manage/my_responses/'


class ResponseDelete(PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('bulletinboard.delete_response',)
    model = Response
    template_name = 'resp_delete.html'
    success_url = '/posts/resp_manage/'


@login_required
def my_responses(request):
    user = request.user
    context = {'responses': Response.objects.filter(resp_author__username=user)}
    return render(request, 'my_responses.html', context)


@login_required
def response_status_update(request, pk):
    resp = Response.objects.get(pk=pk)
    resp.status = True
    resp.save()
    send_mail(
        subject=f'Уведомление о изменении статуса отклика',
        message=f'{resp.resp_author}, ваш отклик на пост: "{resp.post.title}" был принят',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[resp.resp_author.email],
    )
    return redirect(reverse_lazy('resp_manage'))


