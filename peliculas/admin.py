from django.contrib import admin
from .models import (
    Genero, Pelicula, PeliculaGenero,
    Reparto, Puntuacion, Reseña,
    LikeReseña, Favorito
)

admin.site.register(Genero)
admin.site.register(Pelicula)
admin.site.register(PeliculaGenero)
admin.site.register(Reparto)
admin.site.register(Puntuacion)
admin.site.register(Reseña)
admin.site.register(LikeReseña)
admin.site.register(Favorito)
