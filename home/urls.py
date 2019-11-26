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

]