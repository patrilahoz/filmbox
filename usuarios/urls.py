#from django.urls import path
#from . import views

#urlpatterns = [
#    path("registrarse/", views.register_view, name="register"),
#    path("perfil/", views.perfil_user, name="perfil_user"),
#]

# path("login/", views.login_view, name="login"),

from django.urls import path
from . import views

urlpatterns = [
    path("registrarse/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),

    # Perfiles
    path("perfil/", views.perfil_user, name="perfil_user"),
    path("perfil/admin/", views.perfil_admin, name="perfil_admin"),
    # path("perfil/moderador/", views.perfil_moderador, name="perfil_moderador"),
]