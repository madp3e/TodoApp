from django.urls import path
from . import views
from django.contrib.auth import views as views_auth

urlpatterns = [
    path("", views.home, name="home"),
    path("delete/<int:pk>/", views.delete, name="delete"),
    path("complete/<int:pk>/", views.complete, name="complete"),
    path("uncomplete/<int:pk>/", views.uncomplete, name="uncomplete"),
    path("detail/<int:pk>/", views.detail, name="detail"),
    path("false_list/", views.false_list, name="false_list"),
    path("true_list/", views.done_list, name="done_list"),
    path("login/", views_auth.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", views_auth.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("password-reset/", views_auth.PasswordResetView.as_view(template_name="password_reset.html"), name="password_reset"),
    path("password-reset/done/", views_auth.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", views_auth.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete", views_auth.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),

]
