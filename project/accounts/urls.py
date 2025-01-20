from django.urls import path
from .views import ConfirmUser, profile, be_author


urlpatterns = [
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('', profile, name='profile'),
    path('be_author/', be_author, name='be_author'),
]
