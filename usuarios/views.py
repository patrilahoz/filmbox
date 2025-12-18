from django.shortcuts import render

def login_view(request): 
    return render(request, "usuarios/login.html")

def perfil_user(request):
    return render(request, "usuarios/perfil_user.html")
