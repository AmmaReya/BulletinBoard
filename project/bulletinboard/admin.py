from django.contrib import admin
from .models import Post, Category, Author, Response, User
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth.admin import GroupAdmin as origGroupAdmin


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'text',
        ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')
    list_display_links = ('category',)


class ResponseInline(admin.StackedInline):
    model = Response
    extra = 1
    readonly_fields = ('resp_author',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_time_in', 'author', 'category', 'title')
    list_filter = ('author', 'category')
    search_fields = ('title', 'category__category')
    list_display_links = ('title',)
    inlines = [ResponseInline]
    save_on_top = True
    form = PostAdminForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_display_links = ('username',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'author')
    list_display_links = ('author',)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'resp_time_in', 'post', 'resp_author')
    list_display_links = ('resp_author', 'post')
    list_filter = ('resp_author',)
    search_fields = ('post',)
