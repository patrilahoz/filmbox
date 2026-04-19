from django.urls import path, include
from . import views
from .views import add_movie

urlpatterns = [
    path("home/", views.home, name="home"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("pelicula/<int:id>/", views.pelicula, name="pelicula"),
    path("select/", views.select_movie, name="select_movie"),
    path("add/", views.add_movie, name="add_movie"),
]