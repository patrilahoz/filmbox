from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_movie, name="add_movie"),
    path("pelicula/", views.pelicula, name="pelicula"),
    path("select/", views.select_movie, name="select_movie"),
]
