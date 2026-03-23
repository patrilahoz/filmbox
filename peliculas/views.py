from django.shortcuts import render
from .models import Pelicula

def home(request):
    peliculas = Pelicula.objects.all()
    return render(request, "peliculas/home.html", {"peliculas": peliculas})

def add_movie(request):
    return render(request, "peliculas/add_movie.html")

def pelicula(request): 
    return render(request, "peliculas/pelicula.html")

def select_movie(request):
    return render(request, "peliculas/select_movie.html")
