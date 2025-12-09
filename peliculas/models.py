from django.db import models
from usuarios.models import Usuario

class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Pelicula(models.Model):
    titulo = models.CharField(max_length=200)
    año = models.IntegerField()
    director = models.CharField(max_length=100, blank=True)
    duracion_min = models.IntegerField()
    descripcion = models.TextField(blank=True)
    poster_url = models.CharField(max_length=255, blank=True)
    generos = models.ManyToManyField(Genero, through='PeliculaGenero', related_name='peliculas')

    def __str__(self):
        return self.titulo


class PeliculaGenero(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('pelicula', 'genero')


class Reparto(models.Model):
    ROLES = [
        ('actor', 'Actor'),
        ('actriz', 'Actriz'),
    ]
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=6, choices=ROLES)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='reparto')


class Puntuacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    puntuacion = models.DecimalField(max_digits=2, decimal_places=1)  # 0.0 – 9.9
    fecha_puntuacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'pelicula')


class Reseña(models.Model):
    ESTADOS = [
        ('visible', 'Visible'),
        ('oculta', 'Oculta'),
        ('eliminada', 'Eliminada'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_reseña = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=9, choices=ESTADOS, default='visible')


class LikeReseña(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    reseña = models.ForeignKey(Reseña, on_delete=models.CASCADE)
    fecha_like = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'reseña')


class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'pelicula')