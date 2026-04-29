from django.urls import path
from . import views

urlpatterns = [
    path("", views.register_view, name="register"),  # ← ESTA ES LA NUEVA PÁGINA PRINCIPAL
    path("registrarse/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),

    path("perfil/", views.perfil, name="perfil"),
    
    
    path("diario/", views.diario, name="diario"),
    path('editar-perfil/', views.edit_profile, name='edit_profile'),
    
]



# path("perfil/moderador/", views.perfil_moderador, name="perfil_moderador"),
