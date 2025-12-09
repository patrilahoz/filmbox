from django.db import models
from usuarios.models import Usuario
from peliculas.models import Pelicula

class Lista(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre_lista = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre_lista} ({self.usuario})'


class PeliculaEnLista(models.Model):
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE, related_name='items')
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lista', 'pelicula')