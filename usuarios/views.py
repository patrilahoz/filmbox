from django.shortcuts import render

def register_view(request):
    return render(request, "usuarios/registrarse.html")

def perfil_user(request):
    return render(request, "usuarios/perfil_user.html")

# Vista de inicio de sesión (login real)
# def login_view(request):
#    return render(request, "usuarios/login.html")
#