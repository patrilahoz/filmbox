# from django.shortcuts import render
# def register_view(request):
#    return render(request, "usuarios/registrarse.html")
# def perfil_user(request):
#    return render(request, "usuarios/perfil_user.html")

# Vista de inicio de sesión (login real)
# def login_view(request):
#    return render(request, "usuarios/login.html")


from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

User = get_user_model()

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


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "usuarios/login.html", {
                "error": "Correo no registrado"
            })

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user is None:
            return render(request, "usuarios/login.html", {
                "error": "Contraseña incorrecta"
            })

        login(request, user)
        return redirect("home")

    return render(request, "usuarios/login.html")


from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()

@login_required
def perfil_user(request):
    return render(request, "usuarios/perfil_user.html")

@login_required
def perfil_admin(request):
    return render(request, "usuarios/perfil_admin.html")

# @login_required
# def perfil_moderador(request):
#    return render(request, "usuarios/perfil_moderador.html")