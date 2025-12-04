from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('usuario', 'Usuario'),
        ('moderador', 'Moderador'),
        ('administrador', 'Administrador'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')
