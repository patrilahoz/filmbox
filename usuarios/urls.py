from django.urls import path
from . import views

urlpatterns = [
    path("perfil/", views.perfil_user, name="perfil_user"),
]
