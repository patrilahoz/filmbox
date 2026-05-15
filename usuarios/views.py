from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ProfileForm
from peliculas.models import Reseña, Pelicula
from listas.models import Lista

User = get_user_model()


# REGISTRO
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password != password2:
            return render(request, "usuarios/registrarse.html", {
                "error": "Las contraseñas no coinciden"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "usuarios/registrarse.html", {
                "error": "El usuario ya existe"
            })

        if User.objects.filter(email=email).exists():
            return render(request, "usuarios/registrarse.html", {
                "error": "El correo ya está registrado"
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "usuarios/registrarse.html")


# LOGIN
def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is None:
            return render(request, "usuarios/login.html", {
                "error": "Correo o contraseña incorrectos"
            })

        login(request, user)
        return redirect("home")

    return render(request, "usuarios/login.html")


def logout_view(request):
    logout(request)          # Cierra la sesión del usuario
    return redirect('login') # Redirige a la URL con name="login"





# PERFIL
@login_required
def perfil(request):
    qs = (Lista.objects
          .filter(usuario=request.user)
          .prefetch_related('items__pelicula')
          .order_by('-fecha_creacion'))
    mis_listas = []
    for lista in qs:
        all_items = list(lista.items.all())
        mis_listas.append({
            'lista': lista,
            'preview': all_items[:3],
            'count': len(all_items),
        })
    ctx = {'mis_listas': mis_listas}
    if request.user.is_staff:
        return render(request, "usuarios/perfil_admin.html", ctx)
    return render(request, "usuarios/perfil_user.html", ctx)


# EDITAR PERFIL
@login_required
def edit_profile(request):
    profile = request.user.profile
    peliculas = Pelicula.objects.all().order_by('titulo')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('profile_image')

        if not name or not description:
            return render(request, 'usuarios/edit_profile.html', {
                'form': ProfileForm(instance=profile),
                'peliculas': peliculas,
                'error': 'Debes rellenar todos los campos.'
            })

        profile.name = name
        profile.description = description

        if image:
            profile.profile_image = image

        for i in range(1, 5):
            slot = f'fav{i}'
            val = request.POST.get(slot, '').strip()
            if val:
                try:
                    setattr(profile, slot, Pelicula.objects.get(pk=int(val)))
                except (Pelicula.DoesNotExist, ValueError):
                    setattr(profile, slot, None)
            else:
                setattr(profile, slot, None)

        profile.save()
        return redirect('perfil')

    form = ProfileForm(instance=profile)
    return render(request, 'usuarios/edit_profile.html', {'form': form, 'peliculas': peliculas})


# DIARIO
@login_required
def diario(request):
    reseñas = Reseña.objects.filter(usuario=request.user).order_by('-fecha')

    return render(request, "usuarios/diario.html", {
        "reseñas": reseñas
    })