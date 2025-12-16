from django.shortcuts import render

def perfil_user(request):
    return render(request, "usuarios/perfil_user.html")
