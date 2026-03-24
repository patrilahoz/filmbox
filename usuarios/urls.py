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
    path("", views.register_view, name="register"),  # ← ESTA ES LA NUEVA PÁGINA PRINCIPAL
    path("registrarse/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),

    path("perfil/", views.perfil, name="perfil"),


    path("perfil/editar/", views.edit_profile, name="edit_profile"),
]



# path("perfil/moderador/", views.perfil_moderador, name="perfil_moderador"),
