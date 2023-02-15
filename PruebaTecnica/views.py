from django.shortcuts import render,  redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import json
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Estudiante, Curso, DetalleInscripcion
from django.views.generic import View
from dal import autocomplete
from PruebaTecnica.forms import NombreEstudianeForm, NombreCursoForm
from django.contrib import messages
from django.db.models import Avg, Count, Min, Sum
from datetime import date, timedelta
# Create your views here.


def login(request):
    return render(request,'login.html',{})

@login_required()
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

""" REQUEST AJAX """
def loginUser(request):
    username= request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return HttpResponse(json.dumps({"message": "Success"}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message": "inactive"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"message": "invalid"}),content_type="application/json")


@login_required()
def index(request):
    current_date = date.today()
    months_ago = 6
    six_month_previous_date = current_date - timedelta(days=(months_ago * 365 / 12))

    cursostop = DetalleInscripcion.objects.values('curso__nombre').filter(timestamp__gte=six_month_previous_date).annotate(num_estudiantes = Count('curso')).order_by('curso')[:3]
    estudiantes = DetalleInscripcion.objects.values('estudiante__nombre', 'estudiante__apellido_paterno',
                                                    'estudiante__apellido_materno', 'estudiante_id').annotate(num_cursos = Count('estudiante')).order_by('estudiante')

    context = {
        'cursostop': cursostop,
        'estudiantes': estudiantes,
    }

    return render(request, 'dashboard.html', context)


@login_required()
def listadocursos(request, pk):
    estudiante = Estudiante.objects.get(id=pk)
    cursos = DetalleInscripcion.objects.values('curso__nombre', 'curso__fechaInicio', 'curso__fechaFin',
                                               'curso__horario_inicio', 'curso__horario_fin').filter(estudiante_id = pk)
    context = {
        'estudiante': estudiante,
        'cursos' : cursos
    }

    return render(request, 'listado_cursos.html', context)

@login_required()
def profile(request):
    return render(request, 'profile_settings.html', locals())

def logout_view(request):
    logout(request)
    return redirect('/')

""" CRUD ESTUDIANTE """ 

@login_required()
def gestionarestudiante(request):
    estudiantes_list = Estudiante.objects.all()

    paginator = Paginator(estudiantes_list, 10)
    page_number = request.GET.get('page')

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''
    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''
    
    context = {
        'next_url': next_url,
        'prev_url': prev_url,
        'page': page
    }
    return render(request, 'gestionarestudiante.html',context)


@login_required()
def buscarestudiante(request):
    query = request.GET.get('nombre')
   
    if request.method == 'GET':
        estudiantes_list = Estudiante.objects.values('nombre', 'apellido', 'edad', 'email','id').order_by('-edad').filter( Q(nombre=query))
    
   
    paginator = Paginator(estudiantes_list, 10)
    page_number = request.GET.get('page')

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''
    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''
    
    context = {
        'next_url': next_url,
        'prev_url': prev_url,
        'page': page,
        'query': query,
    }
    return render(request, 'gestionarestudiante.html',context)


class CreateCrudEstudiante(View):
    def  get(self, request):
        id_nombre = request.GET.get('id_nombre', None)
        id_paterno = request.GET.get('id_paterno', None)
        id_materno = request.GET.get('id_materno', None)
        id_correo = request.GET.get('id_correo', None)
        id_edad = request.GET.get('id_edad', None)

        obj = Estudiante.objects.create(nombre = id_nombre, apellido_paterno = id_paterno,
                                        apellido_materno = id_materno, edad = id_edad,
                                        email = id_correo)

        estudiantes = {'id':obj.id,'nombre':obj.nombre, 'apellido_paterno':obj.apellido_paterno,'apellido_materno':obj.apellido_materno, 'edad':obj.edad,'email':obj.email }

        data = {
            'estudiantes': estudiantes
        }
        return JsonResponse(data)
    
    
class UpdateCrudEstudiante(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        id_nombre = request.GET.get('id_nombre', None)
        id_paterno = request.GET.get('id_paterno', None)
        id_materno = request.GET.get('id_materno', None)
        id_correo = request.GET.get('id_correo', None)
        id_edad = request.GET.get('id_edad', None)

        obj = Estudiante.objects.get(id=id1)
        obj.nombre = id_nombre
        obj.apellido_paterno = id_paterno
        obj.apellido_materno = id_materno
        obj.edad = id_edad
        obj.email = id_correo
        obj.save()

        estudiantes = {'id':obj.id,'nombre':obj.nombre, 'apellido_paterno':obj.apellido_paterno,'apellido_materno':obj.apellido_materno, 'edad':obj.edad,'email':obj.email }

        data = {
            'estudiantes': estudiantes
        }
       
        return JsonResponse(data)
    
class DeleteCrudEstudiante(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Estudiante.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


""" CRUD CURSO """ 

@login_required()
def gestionarcurso(request):
    cursos_list = Curso.objects.all()
    paginator = Paginator(cursos_list, 10)
    page_number = request.GET.get('page')

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''
    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''
    
    context = {
        'next_url': next_url,
        'prev_url': prev_url,
        'page': page,
    }
    return render(request, 'gestionarcurso.html',context)


class CreateCrudCurso(View):
    def  get(self, request):
        id_nombre = request.GET.get('id_nombre', None)
        id_fecha_inicio = request.GET.get('id_fecha_inicio', None)
        id_hora_inicio = request.GET.get('id_hora_inicio', None)
        id_fecha_fin = request.GET.get('id_fecha_fin', None)
        id_hora_fin = request.GET.get('id_hora_fin', None)

        obj = Curso.objects.create(nombre = id_nombre, fechaInicio = id_fecha_inicio,
                                        horario_inicio = id_hora_inicio, fechaFin = id_fecha_fin,
                                        horario_fin = id_hora_fin)

        cursos = {'id':obj.id,'nombre':obj.nombre, 'horario_inicio':obj.horario_inicio,
                  'horario_fin':obj.horario_fin, 'fechaInicio':obj.fechaInicio,'fechaFin':obj.fechaFin }

        data = {
            'cursos': cursos
        }
        return JsonResponse(data)

class UpdateCrudCurso(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        id_nombre = request.GET.get('id_nombre', None)
        id_fecha_inicio = request.GET.get('id_fecha_inicio', None)
        id_hora_inicio = request.GET.get('id_horario_inicio', None)
        id_fecha_fin = request.GET.get('id_fecha_fin', None)
        id_hora_fin = request.GET.get('id_horario_fin', None)

        obj = Curso.objects.get(id=id1)
        obj.nombre = id_nombre
        obj.fechaInicio = id_fecha_inicio
        obj.horario_inicio = id_hora_inicio
        obj.fechaFin = id_fecha_fin
        obj.horario_fin = id_hora_fin
        obj.save()

        cursos = {'id':obj.id,'nombre':obj.nombre, 'horario_inicio':obj.horario_inicio,'horario_fin':obj.horario_fin, 'fechaInicio':obj.fechaInicio,'fechaFin':obj.fechaFin }

        data = {
            'cursos': cursos
        }
       
        return JsonResponse(data)
    
class DeleteCrudCurso(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Curso.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
    

""" CRUD INSCRIPCION DE CURSO """ 

@login_required()
def gestionarInscripcion(request):
    estudiantes = Estudiante.objects.all()
    cursos = Curso.objects.all()

    inscripciones_list = DetalleInscripcion.objects.all()

    paginator = Paginator(inscripciones_list, 10)
    page_number = request.GET.get('page')

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''
    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    context = {
        'next_url': next_url,
        'prev_url': prev_url,
        'page': page,
        "estudiantes" : estudiantes,
        "cursos" : cursos 
    }

    return render(request, 'gestionarinscripcion.html', context)

@login_required()
def RegistrarInsrcripcion(request):
    if request.method == 'POST':
        idEstudiante = request.POST['estudianteid']
        idCurso = request.POST['cursoid']
        try:
            inscripcion = DetalleInscripcion.objects.filter(curso_id=idCurso, estudiante_id=idEstudiante).values()
            if inscripcion:
                messages.info(request, 'Ya tienes el curso registrado, ¡SIGUE ESTUDIANDO!')
                return redirect('gestionarinscripciones')
            else:
                DetalleInscripcion.objects.create(curso_id=idCurso, estudiante_id=idEstudiante)
                messages.success(request, 'Curso registrado satisfactoriamente, ¡BIENVENIDO!')
               
        except:
                render(request, 'gestionarinscripcion.html')

    return redirect('gestionarinscripciones')


class NombreEstudianteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Estudiante.objects.none()
        qs = Estudiante.objects.all()

        if self.q:
            qs = qs.filter(nombre__istartswith=self.q)

        return qs
    
class NombreCursoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Curso.objects.none()
        qs = Curso.objects.all()

        if self.q:
            qs = qs.filter(nombre__istartswith=self.q)

        return qs



class DeleteCrudInscripcionCurso(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        DetalleInscripcion.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
    