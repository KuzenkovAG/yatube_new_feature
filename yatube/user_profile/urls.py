from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', login_required(views.UserProfile.as_view()), name='index'),
    path(
        'edit/',
        login_required(views.UserChangeDataView.as_view()),
        name='edit'
    ),
    path(
        'follows/',
        login_required(views.UserFollows.as_view()),
        name='follows'
    ),
    path(
        'followers/',
        login_required(views.UserFollowers.as_view()),
        name='followers'
    ),
]
