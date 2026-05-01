from django.urls import path, include
from . import views
from .views import add_movie

urlpatterns = [
    path("home/", views.home, name="home"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("pelicula/<int:pelicula_id>/", views.pelicula, name="pelicula"),

    path('pelicula/<int:pelicula_id>/guardar-reseña/', views.guardar_reseña, name='guardar_reseña'),

    path("reseña/<int:reseña_id>/editar/", views.editar_reseña, name="editar_reseña"),
    path("pelicula/<int:pelicula_id>/cancelar-edicion/", views.cancelar_edicion_reseña, name="cancelar_edicion_reseña"),
    path("reseña/<int:reseña_id>/eliminar/", views.eliminar_reseña, name="eliminar_reseña"),

    path("pelicula/<int:pelicula_id>/editar/", views.editar_pelicula, name="editar_pelicula"),
    path("pelicula/<int:pelicula_id>/eliminar/", views.eliminar_pelicula, name="eliminar_pelicula"),


    path("select/", views.select_movie, name="select_movie"),
    path("add/", views.add_movie, name="add_movie"),
]