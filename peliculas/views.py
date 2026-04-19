from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from peliculas.forms import PeliculaForm
from .models import Pelicula, Genero

@login_required
def home(request):
    peliculas = Pelicula.objects.all()
    return render(request, "peliculas/home.html", {"peliculas": peliculas})

@login_required
def add_movie(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        year = request.POST.get("año")
        director = request.POST.get("director")
        duracion = request.POST.get("duracion_min")
        reparto = request.POST.get("reparto_info")
        synopsis = request.POST.get("sinopsis")
        genres = request.POST.getlist("generos")  # si usas selector múltiple
        poster_file = request.FILES.get("poster")  # ← IMPORTANTE

        # Crear película
        pelicula = Pelicula.objects.create(
            titulo=titulo,
            año=year,
            director=director,
            duracion_min=duracion,
            sinopsis=synopsis,
            reparto_info=reparto,
            poster=poster_file  # ← se guarda automáticamente en MEDIA_ROOT
        )

        # Procesar géneros (si usas un selector múltiple real)
        # for genero_id in request.POST.getlist("generos"):
        #     pelicula.generos.add(genero_id)
        for genero_id in genres:
            pelicula.generos.add(genero_id)

    

        return redirect("home")

    # Si GET → mostrar formulario
    return render(request, "peliculas/add_movie.html", {
        "form": PeliculaForm()  # si usas ModelForm para géneros
    })


#if genres:
#            lista_generos = [g.strip() for g in genres.split(",")]
#            for g in lista_generos:
#                genero_obj, _ = Genero.objects.get_or_create(nombre=g)
#                pelicula.generos.add(genero_obj)
#       return redirect("home")

@login_required
def pelicula(request, id):
    pelicula = Pelicula.objects.get(id=id)
    return render(request, "peliculas/pelicula.html", {"pelicula": pelicula})

@login_required
def catalogo(request):
    peliculas = Pelicula.objects.all()
    return render(request, "peliculas/catalogo.html", {"peliculas": peliculas})

@login_required
def select_movie(request):
    return render(request, "peliculas/select_movie.html")