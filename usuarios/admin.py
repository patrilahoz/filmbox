from django.contrib import admin
from .models import Profile, Usuario, Seguimiento

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description', 'profile_image', 'fav1', 'fav2', 'fav3', 'fav4')

admin.site.register(Usuario)
admin.site.register(Seguimiento)

