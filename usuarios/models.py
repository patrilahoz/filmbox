from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('usuario', 'Usuario'),
        ('moderador', 'Moderador'),
        ('administrador', 'Administrador'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')

    def __str__(self):
        return self.username


class Seguimiento(models.Model):
    seguidor = models.ForeignKey(
        Usuario,
        related_name='seguidos',
        on_delete=models.CASCADE
    )
    seguido = models.ForeignKey(
        Usuario,
        related_name='seguidores',
        on_delete=models.CASCADE
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seguidor.username} sigue a {self.seguido.username}"