import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProfileForm
from .models import Seguimiento
from peliculas.models import Reseña, Pelicula, ReseñaEliminada
from listas.models import Lista

User = get_user_model()


# COMPROBAR DISPONIBILIDAD DE USERNAME
def check_username(request):
    username = request.GET.get('username', '').strip()
    exists = User.objects.filter(username__iexact=username).exists()
    return JsonResponse({'exists': exists})


# COMPROBAR DISPONIBILIDAD DE EMAIL
def check_email(request):
    email = request.GET.get('email', '').strip()
    exists = User.objects.filter(email__iexact=email).exists()
    return JsonResponse({'exists': exists})


# REGISTRO
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if not (3 <= len(username) <= 20):
            return render(request, "usuarios/registrarse.html", {
                "error": "El nombre de usuario debe tener entre 3 y 20 caracteres"
            })

        if not re.fullmatch(r'[a-zA-Z0-9]+', username):
            return render(request, "usuarios/registrarse.html", {
                "error": "El nombre de usuario solo puede contener letras y números"
            })

        if password != password2:
            return render(request, "usuarios/registrarse.html", {
                "error": "Las contraseñas no coinciden"
            })

        password_errors = []
        if len(password) < 12:
            password_errors.append("al menos 12 caracteres")
        if not re.search(r'[A-Z]', password):
            password_errors.append("al menos una mayúscula")
        if not re.search(r'[a-z]', password):
            password_errors.append("al menos una minúscula")
        if not re.search(r'[0-9]', password):
            password_errors.append("al menos un número")
        if not re.search(r'[^a-zA-Z0-9]', password):
            password_errors.append("al menos un símbolo")
        if password_errors:
            return render(request, "usuarios/registrarse.html", {
                "error": "La contraseña debe tener: " + ", ".join(password_errors) + "."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "usuarios/registrarse.html", {
                "error": "El usuario ya existe"
            })

        if not re.fullmatch(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', email):
            return render(request, "usuarios/registrarse.html", {
                "error": "Introduce un correo válido con dominio (.com, .es, .net…)"
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
            'preview': all_items[:5],
            'count': len(all_items),
        })
    ctx = {'mis_listas': mis_listas}
    if request.user.is_staff:
        return render(request, "usuarios/perfil_admin.html", ctx)
    if request.user.rol == 'moderador':
        eliminadas = ReseñaEliminada.objects.filter(eliminada_por=request.user)
        return render(request, "usuarios/perfil_moderador.html", {
            "resenas_eliminadas": eliminadas[:8],
            "total_eliminadas": eliminadas.count(),
        })
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
        elif request.POST.get('remove_profile_image') == '1' and profile.profile_image:
            profile.profile_image.delete(save=False)
            profile.profile_image = None

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


# VER PERFIL DE OTRO USUARIO
@login_required
def ver_perfil(request, username):
    usuario = get_object_or_404(User, username=username)
    qs = (Lista.objects
          .filter(usuario=usuario)
          .prefetch_related('items__pelicula')
          .order_by('-fecha_creacion'))
    mis_listas = []
    for lista in qs:
        all_items = list(lista.items.all())
        mis_listas.append({
            'lista': lista,
            'preview': all_items[:5],
            'count': len(all_items),
        })
    ya_sigue = Seguimiento.objects.filter(seguidor=request.user, seguido=usuario).exists()
    return render(request, 'usuarios/ver_perfil.html', {
        'perfil_usuario': usuario,
        'mis_listas': mis_listas,
        'ya_sigue': ya_sigue,
    })


# SEGUIMIENTOS (lista de seguidos y seguidores)
@login_required
def seguimientos(request, username):
    usuario = get_object_or_404(User, username=username)
    tab = request.GET.get('tab', 'siguiendo')
    siguiendo = User.objects.filter(seguidores__seguidor=usuario)
    seguidores = User.objects.filter(seguidos__seguido=usuario)
    ids_seguidos = set(Seguimiento.objects.filter(seguidor=request.user).values_list('seguido_id', flat=True))
    ids_que_te_siguen = set(Seguimiento.objects.filter(seguido=request.user).values_list('seguidor_id', flat=True))
    return render(request, 'usuarios/seguimientos.html', {
        'perfil_usuario': usuario,
        'tab': tab,
        'siguiendo': siguiendo,
        'seguidores': seguidores,
        'ids_seguidos': ids_seguidos,
        'ids_que_te_siguen': ids_que_te_siguen,
    })


# SEGUIR / DEJAR DE SEGUIR
@login_required
def seguir(request, username):
    usuario_a_seguir = get_object_or_404(User, username=username)
    if request.user != usuario_a_seguir:
        seguimiento, created = Seguimiento.objects.get_or_create(
            seguidor=request.user,
            seguido=usuario_a_seguir
        )
        if not created:
            seguimiento.delete()
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('ver_perfil', username=username)


# DIARIO
@login_required
def diario(request):
    reseñas = Reseña.objects.filter(usuario=request.user).order_by('-fecha')

    return render(request, "usuarios/diario.html", {
        "reseñas": reseñas
    })