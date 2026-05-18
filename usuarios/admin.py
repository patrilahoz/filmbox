from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Usuario, Seguimiento

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ("email", "username", "rol", "is_staff", "is_active")
    list_filter = ("rol", "is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información personal", {"fields": ("username", "rol")}),
        ("Permisos", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "rol", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("email", "username")
    ordering = ("email",)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description', 'profile_image', 'fav1', 'fav2', 'fav3', 'fav4')

admin.site.register(Seguimiento)

