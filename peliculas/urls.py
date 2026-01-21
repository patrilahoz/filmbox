from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Rutas de usuarios
    path("usuarios/", include("usuarios.urls")),

    # Rutas de películas
    path("add/", views.add_movie, name="add_movie"),
    path("pelicula/", views.pelicula, name="pelicula"),
    path("select/", views.select_movie, name="select_movie"),
]