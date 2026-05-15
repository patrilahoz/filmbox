from django.urls import path
from . import views

urlpatterns = [
    path('', views.mis_listas, name='listas'),
    path('crear/', views.crear_lista, name='crear_lista'),
    path('<int:lista_id>/', views.ver_lista, name='ver_lista'),
    path('<int:lista_id>/editar/', views.editar_lista, name='editar_lista'),
    path('<int:lista_id>/eliminar/', views.eliminar_lista, name='eliminar_lista'),
    path('<int:lista_id>/anadir/<int:pelicula_id>/', views.anadir_pelicula, name='anadir_pelicula'),
    path('<int:lista_id>/quitar/<int:pelicula_id>/', views.quitar_pelicula, name='quitar_pelicula'),
]
