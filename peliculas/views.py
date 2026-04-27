from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from peliculas.forms import PeliculaForm
from .models import Pelicula, Genero, LikeReseña, Reseña

# VISTA HOME
@login_required
def home(request):
    peliculas = Pelicula.objects.all()
    return render(request, "peliculas/home.html", {"peliculas": peliculas})

# VISTA AÑADIR PELÍCULA
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


# VISTA PELÍCULA
@login_required
def pelicula(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)

    reseñas = Reseña.objects.filter(pelicula=pelicula).order_by('-fecha')

    return render(request, "peliculas/pelicula.html", {
        "pelicula": pelicula,
        "reseñas": reseñas,
    })



# VISTA CATÁLOGO
@login_required
def catalogo(request):
    peliculas = Pelicula.objects.all().order_by('-id')
    return render(request, "peliculas/catalogo.html", {"peliculas": peliculas})


# VISTA PUNTUACIÓN + RESEÑA
@login_required
def guardar_reseña(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    profile = request.user.profile

    if request.method == "POST":
        puntuacion = request.POST.get("puntuacion")  # 1–5 o vacío
        texto = request.POST.get("reseña")  # texto o vacío

        # Buscar si ya existe reseña del usuario
        reseña, created = Reseña.objects.get_or_create(
            usuario=request.user,
            pelicula=pelicula,
            defaults={"texto": texto, "puntuacion": puntuacion}
        )

        if not created:
            reseña.texto = texto
            reseña.puntuacion = puntuacion
            reseña.save()

        return redirect("pelicula", pelicula_id=pelicula.id)


# VISTA "ME GUSTA" A UNA RESEÑA
@login_required
def like_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, id=reseña_id)

    like, created = LikeReseña.objects.get_or_create(
        usuario=request.user,
        reseña=reseña
    )

    if not created:
        like.delete()  # quitar me gusta

    return redirect("pelicula", pelicula_id=reseña.pelicula.id)
















# VISTA SELECCIONAR PELÍCULA para añadir a favoritos
@login_required
def select_movie(request):
    peliculas = Pelicula.objects.all().order_by('-id')
    return render(request, "peliculas/select_movie.html", {"peliculas": peliculas})