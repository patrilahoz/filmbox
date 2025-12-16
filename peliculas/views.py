from django.shortcuts import render

def home(request):
    return render(request, "peliculas/home.html")

def add_movie(request):
    return render(request, "peliculas/add_movie.html")

def pelicula(request): 
    return render(request, "peliculas/pelicula.html")

def select_movie(request):
    return render(request, "peliculas/select_movie.html")
