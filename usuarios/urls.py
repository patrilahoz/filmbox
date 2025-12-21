from django.urls import path
from . import views

urlpatterns = [
    path("registrarse/", views.register_view, name="register"),
    path("perfil/", views.perfil_user, name="perfil_user"),
]

 # path("login/", views.login_view, name="login"),