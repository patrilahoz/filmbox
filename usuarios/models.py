from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from peliculas.models import Pelicula

# USUARIOS
class Usuario(AbstractUser):
    ROLES = (
        ('usuario', 'Usuario'),
        ('moderador', 'Moderador'),
        ('administrador', 'Administrador'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')

    def __str__(self):
        return self.username


# PERFILES
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    fav1 = models.ForeignKey(Pelicula, on_delete=models.SET_NULL, null=True, blank=True, related_name='fav1_users')
    fav2 = models.ForeignKey(Pelicula, on_delete=models.SET_NULL, null=True, blank=True, related_name='fav2_users')
    fav3 = models.ForeignKey(Pelicula, on_delete=models.SET_NULL, null=True, blank=True, related_name='fav3_users')
    fav4 = models.ForeignKey(Pelicula, on_delete=models.SET_NULL, null=True, blank=True, related_name='fav4_users')

    @property
    def profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return '/media/profile_images/pfp-por-defecto.png'

    def __str__(self):
        return f"Perfil de {self.user.username}"



from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


# PERMISOS MODERADOR
from django.contrib.auth.models import Permission

@receiver(post_save, sender=Usuario)
def asignar_permisos_moderador(sender, instance, created, **kwargs):
    if instance.rol == "moderador":
        permiso = Permission.objects.get(codename="puede_eliminar_reseñas")
        instance.user_permissions.add(permiso)



# SEGUIMIENTOS
class Seguimiento(models.Model):
    seguidor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='seguidos',
        on_delete=models.CASCADE
    )
    seguido = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='seguidores',
        on_delete=models.CASCADE
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seguidor.username} sigue a {self.seguido.username}"
