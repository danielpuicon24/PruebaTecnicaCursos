"""RetoCursos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.urls import re_path as url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, re_path
from django.contrib.auth import views as auth_views

from PruebaTecnica import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name="login"),
    path('', views.logout_view, name="logout"),
    path('index/', views.index, name="index"),
    path('profile/', views.profile, name="profile"),
    path('post/ajax/loginUser', views.loginUser, name='loginUser'),

    url(r'^cursos/(?P<pk>[0-9]+)/$', views.listadocursos, name="cursos"),

    path('estudiante/', views.gestionarestudiante, name="gestionarestudiante"),
    path('ajax/crud/createStudent/',  views.CreateCrudEstudiante.as_view(), name='crud_ajax_create_estudiante'),
    path('ajax/crud/updateStudent/',  views.UpdateCrudEstudiante.as_view(), name='crud_ajax_update_estudiante'),
    path('ajax/crud/deleteStudent/', views.DeleteCrudEstudiante.as_view(), name='deleteStudent'),

    path('curso/', views.gestionarcurso, name="gestionarcurso"),
    path('ajax/crud/createCourse/',  views.CreateCrudCurso.as_view(), name='crud_ajax_create_curso'),
    path('ajax/crud/updateCourse/',  views.UpdateCrudCurso.as_view(), name='crud_ajax_update_curso'),
    path('ajax/crud/deleteCurso/', views.DeleteCrudCurso.as_view(), name='deleteCurso'),

    path('inscripciones/', views.gestionarInscripcion, name="gestionarinscripciones"),
    path('registrarInscripcion/', views.RegistrarInsrcripcion, name="registrarInscripcion"),
    path('ajax/crud/deleteInscripcion/', views.DeleteCrudInscripcionCurso.as_view(), name='deleteInscripcion'),

    re_path(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),

    re_path(
        r'^nombre-estudiante-autocomplete/$',
         views.NombreEstudianteAutocomplete.as_view(),
        name='nombre-estudiante-autocomplete',
    ),

    re_path(
        r'^nombre-curso-autocomplete/$',
         views.NombreCursoAutocomplete.as_view(),
        name='nombre-curso-autocomplete',
    ),
    
]+ static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
