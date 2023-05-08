from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path(
        'group/<slug:slug>/',
        views.GroupListView.as_view(),
        name='group_list'
    ),
    path(
        'profile/<str:username>/',
        views.ProfileListView.as_view(),
        name='profile'
    ),
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path(
        'posts/<int:post_id>/edit/',
        views.PostUpdateView.as_view(),
        name='post_edit'
    ),
    path(
        'posts/<int:post_id>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment'
    ),
    path('follow/', views.FollowsListView.as_view(), name='follow_index'),
    path(
        'profile/<str:username>/follow/',
        views.FollowRedirectView.as_view(),
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.UnFollowRedirectView.as_view(),
        name='profile_unfollow'
    ),
    path('like/<int:post_id>/', views.LikeRedirectView.as_view(), name='like'),
    path(
        'dislike/<int:post_id>/',
        views.DislikeRedirectView.as_view(),
        name='dislike'
    ),
]
