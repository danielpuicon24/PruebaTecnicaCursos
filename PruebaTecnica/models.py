from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# Create your models here.

class Curso(models.Model):
    nombre = models.CharField(max_length=60)
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'curso'
        managed = True
        
    def __str__(self):
        return self.nombre


class Estudiante(models.Model):
    nombre = models.CharField(max_length=60)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    edad = models.IntegerField()
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'estudiante'
        managed = True
        
    def __str__(self):
        return self.nombre
    


class DetalleInscripcion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'detalle_inscripcion'
        managed = True

