from django import forms
from dal import autocomplete
from django.contrib.auth.models import User
from .models import Curso, Estudiante


class NombreEstudianeForm(forms.ModelForm):
    nombre = forms.ModelChoiceField(
        queryset=Estudiante.objects.all(),
        widget=autocomplete.ModelSelect2(url='nombre-estudiante-autocomplete')
    )

    class Meta:
        model = Estudiante
        fields = ('nombre',)

class NombreCursoForm(forms.ModelForm):
    nombre = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        widget=autocomplete.ModelSelect2(url='nombre-curso-autocomplete')
    )

    class Meta:
        model = Curso
        fields = ('nombre',)