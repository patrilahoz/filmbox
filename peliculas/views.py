from urllib import request

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache

from peliculas.forms import PeliculaForm
from .models import Pelicula, Genero, LikeReseña, Reseña, ReseñaEliminada
from listas.models import Lista, PeliculaEnLista
from django.db.models import Max, Count, Avg
from usuarios.models import Seguimiento

# VISTA HOME
@login_required
def home(request):
    peliculas_recientes = (
        Pelicula.objects
        .order_by('-año', '-id')[:10]
    )

    tendencias = (
        Pelicula.objects
        .annotate(num_resenas=Count("reseña"))
        .order_by('-num_resenas')[:10]
    )

    try:
        destacada = Pelicula.objects.get(id=36)
    except Pelicula.DoesNotExist:
        destacada = None

    resenas_recientes = (
        Reseña.objects
        .exclude(texto__isnull=True)
        .exclude(texto='')
        .select_related('usuario', 'pelicula', 'usuario__profile')
        .order_by('-fecha')[:6]
    )

    mejores_peliculas = (
        Pelicula.objects
        .annotate(avg_rating=Avg('reseña__puntuacion'), num_resenas=Count('reseña'))
        .filter(num_resenas__gte=1)
        .order_by('-avg_rating', '-num_resenas')[:10]
    )

    ids_seguidos = Seguimiento.objects.filter(
        seguidor=request.user
    ).values_list('seguido_id', flat=True)

    actividad_seguidos = (
        Reseña.objects
        .filter(usuario_id__in=ids_seguidos)
        .select_related('usuario', 'pelicula', 'usuario__profile')
        .order_by('-fecha')[:5]
    )

    return render(request, "peliculas/home.html", {
        "peliculas": peliculas_recientes,
        "tendencias": tendencias,
        "destacada": destacada,
        "resenas_recientes": resenas_recientes,
        "mejores_peliculas": mejores_peliculas,
        "actividad_seguidos": actividad_seguidos,
    })



# VISTA AÑADIR PELÍCULA
@login_required
def add_movie(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        year = request.POST.get("año")
        director = request.POST.get("director")
        duracion = request.POST.get("duracion_min")
        reparto = request.POST.get("reparto_info")
        synopsis = request.POST.get("sinopsis")
        genres = request.POST.getlist("generos")
        poster_file = request.FILES.get("poster")

        # Crear película
        pelicula = Pelicula.objects.create(
            titulo=titulo,
            año=year,
            director=director,
            duracion_min=duracion,
            sinopsis=synopsis,
            reparto_info=reparto,
            poster=poster_file
        )

        # Procesar géneros (si usas un selector múltiple real)
        # for genero_id in request.POST.getlist("generos"):
        #     pelicula.generos.add(genero_id)
        for genero_id in genres:
            pelicula.generos.add(genero_id)

        return redirect("catalogo")

    # Si GET → mostrar formulario
    return render(request, "peliculas/add_movie.html", {
        "form": PeliculaForm()  # si usas ModelForm para géneros
    })



# VISTA PELÍCULA
@login_required
@never_cache
def pelicula(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)

    # Todas las reseñas ordenadas por fecha
    reseñas_qs = Reseña.objects.filter(pelicula=pelicula).order_by('-fecha')

    # Si el usuario tiene reseña, ponerla la primera
    if request.user.is_authenticated:
        propia = reseñas_qs.filter(usuario=request.user)
        otras = reseñas_qs.exclude(usuario=request.user)
        reseñas = list(propia) + list(otras)
    else:
        reseñas = list(reseñas_qs)


    # Si hay reseña en edición
    edit_id = request.session.get('edit_reseña_id')
    reseña_editando = None
    if edit_id:
        reseña_editando = Reseña.objects.filter(id=edit_id, usuario=request.user).first()

    mis_listas = Lista.objects.filter(usuario=request.user).order_by('nombre_lista')
    listas_con_pelicula = set(
        PeliculaEnLista.objects.filter(
            lista__usuario=request.user,
            pelicula=pelicula
        ).values_list('lista_id', flat=True)
    )
    user_likes = set(
        LikeReseña.objects.filter(
            usuario=request.user,
            reseña__pelicula=pelicula
        ).values_list('reseña_id', flat=True)
    )

    # Distribución de puntuaciones (1-5)
    dist_raw = {
        row['puntuacion']: row['count']
        for row in Reseña.objects
                         .filter(pelicula=pelicula, puntuacion__isnull=False)
                         .values('puntuacion')
                         .annotate(count=Count('id'))
    }
    total_puntuaciones = sum(dist_raw.values())
    distribucion = [
        {
            'estrellas': s,
            'count': dist_raw.get(s, 0),
            'pct': round(dist_raw.get(s, 0) / total_puntuaciones * 100) if total_puntuaciones else 0,
        }
        for s in range(5, 0, -1)
    ]
    avg_puntuacion = (
        round(sum(d['estrellas'] * d['count'] for d in distribucion) / total_puntuaciones, 1)
        if total_puntuaciones else None
    )

    return render(request, "peliculas/pelicula.html", {
        "pelicula": pelicula,
        "reseñas": reseñas,
        "reseña_editando": reseña_editando,
        "mis_listas": mis_listas,
        "listas_con_pelicula": listas_con_pelicula,
        "user_likes": user_likes,
        "distribucion": distribucion,
        "total_puntuaciones": total_puntuaciones,
        "avg_puntuacion": avg_puntuacion,
    })



# VISTA EDITAR PELÍCULA
@login_required
def editar_pelicula(request, pelicula_id):
    if not request.user.is_staff:
        return redirect("home")

    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    form = PeliculaForm()

    if request.method == "POST":
        pelicula.titulo = request.POST.get("titulo")
        pelicula.director = request.POST.get("director")
        pelicula.año = request.POST.get("año")
        pelicula.duracion_min = request.POST.get("duracion_min")
        pelicula.sinopsis = request.POST.get("sinopsis")
        pelicula.reparto_info = request.POST.get("reparto_info")

        poster_file = request.FILES.get("poster")
        remove_poster = request.POST.get("remove_poster") == "1"

        if poster_file:
            pelicula.poster = poster_file
        elif remove_poster and pelicula.poster:
            pelicula.poster.delete(save=False)
            pelicula.poster = None

        pelicula.save()

        pelicula.generos.clear()
        for genero_id in request.POST.getlist("generos"):
            pelicula.generos.add(genero_id)

        return redirect("pelicula", pelicula_id=pelicula.id)

    return render(request, "peliculas/add_movie.html", {
        "form": form,
        "pelicula": pelicula,
        "is_editing": True,
        "selected_generos": list(pelicula.generos.values_list("id", flat=True))
    })


# VISTA ELIMINAR PELÍCULA
@login_required
def eliminar_pelicula(request, pelicula_id):
    if not request.user.is_staff:
        return redirect("home")

    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    pelicula.delete()

    return redirect("catalogo")



# VISTA PUNTUACIÓN + RESEÑA Y GUARDAR RESEÑA
@login_required
def guardar_reseña(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)

    if request.method == "POST":
        puntuacion = request.POST.get("puntuacion") or None
        texto = request.POST.get("reseña")

        edit_id = request.session.get('edit_reseña_id')

        if edit_id:
            reseña = get_object_or_404(Reseña, id=edit_id, usuario=request.user)
            reseña.texto = texto
            reseña.puntuacion = puntuacion
            reseña.save()
            del request.session['edit_reseña_id']

        else:
            reseña, created = Reseña.objects.get_or_create(
                usuario=request.user,
                pelicula=pelicula,
                defaults={"texto": texto, "puntuacion": puntuacion}
            )

            if not created:
                reseña.texto = texto
                reseña.puntuacion = puntuacion
                reseña.save()

        return redirect("pelicula", pelicula_id=pelicula.id)




# VISTA EDITAR RESEÑA
@login_required
def editar_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, id=reseña_id, usuario=request.user)
    
    # Guardamos en sesión qué reseña se está editando
    request.session['edit_reseña_id'] = reseña.id
    
    return redirect("pelicula", pelicula_id=reseña.pelicula.id)


# VISTA CANCELAR EDITAR RESEÑA
@login_required
def cancelar_edicion_reseña(request, pelicula_id):
    request.session.pop('edit_reseña_id', None)
    return redirect("pelicula", pelicula_id=pelicula_id)



# VISTA ELIMINAR RESEÑA
@login_required
def eliminar_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, id=reseña_id)

    # Moderador: puede eliminar cualquier reseña y se registra en el log
    if request.user.has_perm("peliculas.puede_eliminar_reseñas"):
        pelicula_id = reseña.pelicula.id
        ReseñaEliminada.objects.create(
            pelicula_titulo=reseña.pelicula.titulo,
            autor_username=reseña.usuario.username,
            eliminada_por=request.user,
        )
        reseña.delete()
        return redirect("pelicula", pelicula_id=pelicula_id)

    # Superuser: puede eliminar cualquier reseña
    if request.user.is_superuser:
        pelicula_id = reseña.pelicula.id
        reseña.delete()
        return redirect("pelicula", pelicula_id=pelicula_id)

    # Usuario estándar o administrador: solo puede eliminar su propia reseña
    if reseña.usuario != request.user:
        return HttpResponseForbidden("No puedes eliminar reseñas de otros usuarios.")

    pelicula_id = reseña.pelicula.id
    reseña.delete()
    return redirect("pelicula", pelicula_id=pelicula_id)


# VISTA TODAS LAS RESEÑAS (solo moderadores)
@login_required
def todas_resenas(request):
    if not request.user.has_perm("peliculas.puede_eliminar_reseñas") and not request.user.is_superuser:
        return HttpResponseForbidden()

    reseñas = (
        Reseña.objects
        .select_related('usuario', 'pelicula')
        .order_by('-fecha')
    )

    q = request.GET.get('q', '').strip()
    if q:
        reseñas = reseñas.filter(pelicula__titulo__icontains=q)

    return render(request, "peliculas/todas_resenas.html", {
        "reseñas": reseñas,
        "q": q,
    })



# VISTA "ME GUSTA" A UNA RESEÑA
@login_required
def like_reseña(request, reseña_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'method not allowed'}, status=405)

    reseña = get_object_or_404(Reseña, id=reseña_id)

    like, created = LikeReseña.objects.get_or_create(
        usuario=request.user,
        reseña=reseña
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'count': reseña.likereseña_set.count()})



# VISTA CATÁLOGO
@login_required
def catalogo(request):
    peliculas = Pelicula.objects.all().order_by('titulo')

    # Buscador por título
    q = request.GET.get("q")
    if q:
        peliculas = peliculas.filter(titulo__icontains=q)

    # Filtro por género desde home (ej: ?genero=Comedia)
    genero_nombre = request.GET.get("genero")
    if genero_nombre:
        peliculas = peliculas.filter(generos__nombre__icontains=genero_nombre)

    # Filtro por géneros (lista de IDs desde el desplegable)
    generos_seleccionados = request.GET.getlist("generos")
    if generos_seleccionados:
        peliculas = peliculas.filter(generos__id__in=generos_seleccionados).distinct()

    # Lista de géneros para el desplegable
    generos = Genero.objects.all()

    return render(request, "peliculas/catalogo.html", {
        "peliculas": peliculas,
        "generos": generos,
        "generos_seleccionados": generos_seleccionados,
        "q": q,
        "genero_nombre": genero_nombre,
    })





# VISTA SELECCIONAR PELÍCULA para añadir a favoritos
@login_required
def select_movie(request):
    peliculas = Pelicula.objects.all().order_by('-id')
    return render(request, "peliculas/select_movie.html", {"peliculas": peliculas})