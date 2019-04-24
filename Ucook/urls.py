from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import login, logout
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from . import views

urlpatterns = [
    # need to change the path
    path('', views.login_action, name='home'),
    path('login', views.login_action, name='login'),
    path('login/', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('welcome', views.welcome_action, name='welcome'),
    path('register', views.register_action, name='register'),
    path('iAmHost', views.welcome_host_action, name='iAmHost'),
    path('iAmNonHost', views.welcome_guest_action, name='iAmNonHost'),
    path('exploreHost', views.explorehost_action, name='exploreHost'),
    path('exploreNonHost', views.explore_guest_action, name='exploreNonHost'),
    path('profile', views.profile_action, name='profile'),
    path('detail', views.detail_action, name='detail'),
    path('mypost', views.mypost_action, name='mypost'),
    path('comment', views.comment_action, name='comment'),
    path('post-host-detail', views.post_host_action, name='post-host-detail'),
    path('post-guest-detail', views.post_guest_action, name='post-guest-detail'),

    # url(r'^reset-password/$', PasswordResetView.as_view(), name='reset_password'),
    # url(r'^reset-password/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # url(r'^reset-password/complete/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    url(r"^paypal/", include("paypal.standard.ipn.urls")),
    path("getClosestPosts", views.closest_posts_action, name="get-closest-posts"),
    # path('change-password', views.change_password, name='change_password'),
    # need to create a `registration` folder under `templates`
    url(
        r"^reset-password/$",
        PasswordResetView.as_view(),
        {
            "template_name": "registration/password_reset_form.html",
            "email_template_name": "registration/password_reset_subject.txt",
            "html_email_template_name": "registration/password_reset_email.html",
            "subject_template_name": "registration/password_reset_subject.txt",
        },
        name="reset_password",
    ),
    url(
        r"^reset-password/done/$",
        PasswordResetDoneView.as_view(),
        {"template_name": "registration/password_reset_form.html"},
        name="password_reset_done",
    ),
    url(
        r"^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
        PasswordResetConfirmView.as_view(),
        {"template_name": "registration/password_reset_confirm.html"},
        name="password_reset_confirm",
    ),
    url(
        r"^reset-password/complete/$",
        PasswordResetCompleteView.as_view(),
        {"template_name": "registration/password_reset_done.html"},
        name="password_reset_complete",
    ),
]
