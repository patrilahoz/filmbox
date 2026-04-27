from django.db import models
from django.conf import settings

#GÉNEROS
class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


#PELÍCULAS
class Pelicula(models.Model):
    titulo = models.CharField(max_length=200)
    año = models.IntegerField()
    director = models.CharField(max_length=100, blank=True)
    duracion_min = models.IntegerField()
    reparto_info = models.TextField(blank=True)
    sinopsis = models.TextField(blank=True)


    poster = models.ImageField(upload_to="posters/", blank=True, null=True)

    generos = models.ManyToManyField(
    Genero,
    through='PeliculaGenero',
    related_name='peliculas'
)

    def __str__(self):
        return self.titulo



class PeliculaGenero(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pelicula} - {self.genero}"

    # class Meta:
    #    unique_together = ('pelicula', 'genero')


#REPARTO
class Reparto(models.Model):
    ROLES = [
        ('actor', 'Actor'),
        ('actriz', 'Actriz'),
    ]
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=6, choices=ROLES)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='reparto')


#PUNTUACIONES
class Puntuacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    valor = models.IntegerField(null=True, blank=True)  # 1–5
    fecha = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('usuario', 'pelicula')



#RESEÑAS
class Reseña(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    texto = models.TextField(blank=True, null=True)
    puntuacion = models.IntegerField(null=True, blank=True)  # opcional
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']
        unique_together = ('usuario', 'pelicula')



#LIKES RESEÑA
class LikeReseña(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reseña = models.ForeignKey(Reseña, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'reseña')



#FAVORITOS
class Favorito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'pelicula')