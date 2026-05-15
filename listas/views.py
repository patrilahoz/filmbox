from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme

from peliculas.models import Pelicula
from .models import Lista, PeliculaEnLista


@login_required
def mis_listas(request):
    mis_qs = (Lista.objects
              .filter(usuario=request.user)
              .prefetch_related('items__pelicula')
              .order_by('-fecha_creacion'))

    mis_listas_data = []
    for lista in mis_qs:
        all_items = list(lista.items.all())
        mis_listas_data.append({
            'lista': lista,
            'preview': all_items[:3],
            'count': len(all_items),
        })

    comunidad_qs = (Lista.objects
                    .exclude(usuario=request.user)
                    .select_related('usuario')
                    .prefetch_related('items__pelicula')
                    .order_by('-fecha_creacion'))

    comunidad_data = []
    for lista in comunidad_qs:
        all_items = list(lista.items.all())
        comunidad_data.append({
            'lista': lista,
            'preview': all_items[:3],
            'count': len(all_items),
        })

    return render(request, 'listas/listas.html', {
        'mis_listas': mis_listas_data,
        'comunidad': comunidad_data,
    })


@login_required
def crear_lista(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_lista', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        if nombre:
            Lista.objects.create(
                usuario=request.user,
                nombre_lista=nombre,
                descripcion=descripcion,
            )
    return redirect('listas')


@login_required
def ver_lista(request, lista_id):
    lista = get_object_or_404(Lista, id=lista_id)
    items = list(lista.items.select_related('pelicula').order_by('-fecha_agregado'))
    es_mia = lista.usuario == request.user
    todas_peliculas = None
    if es_mia:
        ids_en_lista = [item.pelicula_id for item in items]
        todas_peliculas = Pelicula.objects.exclude(id__in=ids_en_lista).order_by('titulo')
    return render(request, 'listas/ver_lista.html', {
        'lista': lista,
        'items': items,
        'todas_peliculas': todas_peliculas,
        'es_mia': es_mia,
    })


@login_required
def editar_lista(request, lista_id):
    lista = get_object_or_404(Lista, id=lista_id, usuario=request.user)
    if request.method == 'POST':
        nombre = request.POST.get('nombre_lista', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        if nombre:
            lista.nombre_lista = nombre
            lista.descripcion = descripcion
            lista.save()
    return redirect('ver_lista', lista_id=lista.id)


@login_required
def eliminar_lista(request, lista_id):
    lista = get_object_or_404(Lista, id=lista_id, usuario=request.user)
    lista.delete()
    return redirect('listas')


@login_required
def anadir_pelicula(request, lista_id, pelicula_id):
    lista = get_object_or_404(Lista, id=lista_id, usuario=request.user)
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    PeliculaEnLista.objects.get_or_create(lista=lista, pelicula=pelicula)
    next_url = request.POST.get('next', '')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect('ver_lista', lista_id=lista.id)


@login_required
def quitar_pelicula(request, lista_id, pelicula_id):
    lista = get_object_or_404(Lista, id=lista_id, usuario=request.user)
    PeliculaEnLista.objects.filter(lista=lista, pelicula_id=pelicula_id).delete()
    next_url = request.POST.get('next', '')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect('ver_lista', lista_id=lista.id)
