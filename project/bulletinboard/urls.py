from django.urls import path
from .views import *


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('my_posts/', my_posts, name='my_posts'),
    path('resp_manage/', manage_responses, name='resp_manage'),
    path('resp_manage/my_responses/', my_responses, name='my_responses'),
    path('response/<int:pk>/create/', ResponseCreate.as_view(), name='resp_create'),
    path('response/<int:pk>/update/', ResponseUpdate.as_view(), name='resp_update'),
    path('response/<int:pk>/delete/', ResponseDelete.as_view(), name='resp_delete'),
    path('response/<int:pk>/delete_author/', ResponseDeleteAuthor.as_view(), name='resp_delete_author'),
    path('response/<int:pk>/status/', response_status_update, name='resp_status'),


]
