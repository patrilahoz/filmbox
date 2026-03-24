from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import Pelicula, Genero

def home(request):
    peliculas = Pelicula.objects.all()
    return render(request, "peliculas/home.html", {"peliculas": peliculas})

@staff_member_required
def add_movie(request):
    if request.method == "POST":
        titulo = request.POST.get("title")
        director = request.POST.get("director")
        year = request.POST.get("year")
        genres = request.POST.get("genres")
        synopsis = request.POST.get("synopsis")

        # Crear película
        pelicula = Pelicula.objects.create(
            titulo=titulo,
            director=director,
            año=year,
            descripcion=synopsis,
            duracion_min=120,  # temporal si no lo pones en el formulario
            poster_url=""      # lo añadiremos luego
        )

        # Procesar géneros
        if genres:
            lista_generos = [g.strip() for g in genres.split(",")]
            for g in lista_generos:
                genero_obj, _ = Genero.objects.get_or_create(nombre=g)
                pelicula.generos.add(genero_obj)

        return redirect("home")

    return render(request, "peliculas/add_movie.html")


def pelicula(request): 
    return render(request, "peliculas/pelicula.html")

def select_movie(request):
    return render(request, "peliculas/select_movie.html")
