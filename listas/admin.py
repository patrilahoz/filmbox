from django.contrib import admin
from .models import Lista, PeliculaEnLista

# Inline: muestra las películas dentro de cada lista
class PeliculaEnListaInline(admin.TabularInline):
    model = PeliculaEnLista
    extra = 1  # cuántos campos vacíos aparecen por defecto

# Admin de Lista con Inline
@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    list_display = ('nombre_lista', 'usuario', 'fecha_creacion')
    inlines = [PeliculaEnListaInline]

# También puedes registrar PeliculaEnLista por separado si quieres
@admin.register(PeliculaEnLista)
class PeliculaEnListaAdmin(admin.ModelAdmin):
    list_display = ('lista', 'pelicula', 'fecha_agregado')
