from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("perfil/", views.perfil_user, name="perfil_user"),
]