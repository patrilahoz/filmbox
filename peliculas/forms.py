from django import forms
from .models import Pelicula, Genero

class PeliculaForm(forms.ModelForm):
    generos = forms.ModelMultipleChoiceField(
        queryset=Genero.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Pelicula
        fields = [
            "titulo",
            "año",
            "director",
            "duracion_min",
            "reparto_info",
            "poster",
            "generos",
            "sinopsis",
        ]
