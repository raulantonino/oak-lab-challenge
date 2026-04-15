from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "booking"

urlpatterns = [
    path("", views.home_redirect, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("choose-creature/", views.choose_creature, name="choose_creature"),
    path("choose-time-slot/", views.choose_time_slot, name="choose_time_slot"),
]