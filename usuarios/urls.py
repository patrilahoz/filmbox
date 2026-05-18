from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # PÁGINA DE REGISTRO NADA MÁS ABRIR LA APLICACIÓN
    path("", views.register_view, name="register"),

    # PÁGINA DE REGISTRO, LOGIN Y LOGOUT
    path("registrarse/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    # PÁGINA DE PERFIL SEGÚN EL ROL DEL USUARIO
    path("perfil/", views.perfil, name="perfil"),
    
    # PÁGINAS DE DIARIO Y EDICIÓN DE PERFIL
    path("diario/", views.diario, name="diario"),
    path('editar-perfil/', views.edit_profile, name='edit_profile'),
    path('perfil/<str:username>/', views.ver_perfil, name='ver_perfil'),
    path('perfil/<str:username>/seguir/', views.seguir, name='seguir'),

]



# path("perfil/moderador/", views.perfil_moderador, name="perfil_moderador"),
