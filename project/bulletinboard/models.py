from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')

    def __str__(self):
        return f'{self.author.username}'


class Category(models.Model):
    category = models.CharField(max_length=25)

    def __str__(self):
        return self.category


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)
    text = RichTextUploadingField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    resp_author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    resp_time_in = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
