from django.urls import path, include
from . import views
from .views import add_movie

urlpatterns = [
    path("home/", views.home, name="home"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("pelicula/<int:pelicula_id>/", views.pelicula, name="pelicula"),

    path('pelicula/<int:pelicula_id>/guardar-reseña/', 
         views.guardar_reseña, 
         name='guardar_reseña'),

    path("select/", views.select_movie, name="select_movie"),
    path("add/", views.add_movie, name="add_movie"),
]