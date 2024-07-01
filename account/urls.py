from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path("login/", views.user_login, name="login"),
    path("", views.dashboard, name="dashboard"),
    # login/logout urls
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", views.user_logout, name="logout"),
    # change password urls
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    # reset password urls
    path(
        "password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # user registration url
    path("register/", views.user_register, name="register"),
    path("edit/", views.edit, name="edit"),
    path("users/", views.user_list, name="user_list"),
    path("users/follow/", views.user_follow, name="user_follow"),
    path("users/<username>/", views.user_detail, name="user_detail"),
]
