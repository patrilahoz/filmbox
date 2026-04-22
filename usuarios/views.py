from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ProfileForm

User = get_user_model()


# -----------------------------
# REGISTRO
# -----------------------------
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


# -----------------------------
# LOGIN
# -----------------------------
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


# -----------------------------
# PERFIL
# -----------------------------
@login_required
def perfil(request):
    if request.user.is_staff:
        return render(request, "usuarios/perfil_admin.html")
    return render(request, "usuarios/perfil_user.html")


# -----------------------------
# EDITAR PERFIL
# -----------------------------
@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('profile_image')

        # Validación básica (ya la haces en JS, pero por si acaso)
        if not name or not description:
            return render(request, 'usuarios/edit_profile.html', {
                'form': ProfileForm(instance=profile),
                'error': 'Debes rellenar todos los campos.'
            })

        # Guardar datos
        profile.name = name
        profile.description = description

        if image:
            profile.profile_image = image

        profile.save()

        return redirect('perfil')

    # GET
    form = ProfileForm(instance=profile)
    return render(request, 'usuarios/edit_profile.html', {'form': form})
