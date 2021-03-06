# coding: utf-8
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from citasmedicas.serializers import DoctorSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import generics
from django.http import Http404
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from django.template.response import TemplateResponse
from django.http import HttpResponse
from citasmedicas.forms import (ConsultorioForm, LoginForm, PacienteForm,
                                SecretariaEditForm, SecretariaForm)
from citasmedicas.models import Consultorio, Doctor, Paciente, Secretaria


def index(request):
    doctores = Doctor.objects.all()
    return render(request,
                  'citasmedicas/index.html',
                  {'doctores': doctores})


@login_required(login_url='login')
def citasmedicas_index(request):
    return render(request,
                  'citasmedicas/citasmedicas_index.html')


def login_page(request):
    mensaje = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = request.POST['usuario']
            contrasena = request.POST['contrasena']
            user = authenticate(username=usuario, password=contrasena)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('citasmedicas_index'))
                else:
                    mensaje = "Usuario inactivo"
            else:
                mensaje = "Usuario o contraseña incorrecto(a)"
    else:
        form = LoginForm()
    return render(request,
                  'citasmedicas/login.html',
                  {'mensaje': mensaje, 'form': form})


def logout_page(request):
    logout(request)
    return redirect('citasmedicas_index')


@login_required(login_url='login')
def secretaria_alta(request):
    try:
        doctor = Doctor.objects.get(usuario=request.user)
    except Doctor.DoesNotExist:
        doctor = None
        messages.warning(request, "Acceso no autorizado")
        return render(request,
                      'citasmedicas/mensajes_usuarios.html')
    if request.method == "POST":
        form = SecretariaForm(request.POST)
        if form.is_valid():
            secretaria = form.save(commit=False)
            secretaria.doctor = doctor
            usuario = User.objects.create_user(
                username=request.POST['usuario'],
                password=request.POST['contrasena'],
            )
            usuario.save()
            secretaria.usuario = usuario
            secretaria.save()
            return redirect('secretaria_lista')
    else:
        form = SecretariaForm()
    return render(request,
                  'citasmedicas/secretaria_alta.html',
                  {'form': form})


@login_required(login_url='login')
def secretaria_lista(request):
    try:
        doctor = Doctor.objects.get(usuario=request.user)
    except Doctor.DoesNotExist:
        doctor = None
        messages.warning(request, "Acceso no autorizado")
        return render(request,
                      'citasmedicas/mensajes_usuarios.html')
    secretarias = Secretaria.objects.filter(doctor=doctor)
    return render(request, 'citasmedicas/secretaria_lista.html',
                  {'secretarias': secretarias})


@login_required(login_url='login')
def secretaria_edita(request, pk):
    try:
        doctor = Doctor.objects.get(usuario=request.user)
    except Doctor.DoesNotExist:
        doctor = None
        messages.warning(request, "Acceso no autorizado")
        return render(request,
                      'citasmedicas/mensajes_usuarios.html')
    if request.method == "POST":
        form = SecretariaEditForm(request.POST)
        if form.is_valid():
            datos_limpios = form.cleaned_data
            secretaria = Secretaria.objects.get(pk=pk)
            secretaria.nombres = datos_limpios.get('nombres')
            secretaria.apellido_paterno = datos_limpios.get('apellido_paterno')
            secretaria.apellido_materno = datos_limpios.get('apellido_materno')
            secretaria.telefono_personal = datos_limpios.get(
                'telefono_personal')
            secretaria.save()
            return redirect('secretaria_lista')
    else:
        try:
            secretaria = Secretaria.objects.get(pk=pk)
        except Secretaria.DoesNotExist:
            secretaria = None
            messages.warning(request, "La secretaria no existe.")
            return render(request,
                          'citasmedicas/mensajes_usuarios.html')
        form = SecretariaEditForm(instance=secretaria)
    return render(request,
                  'citasmedicas/secretaria_alta.html',
                  {'form': form})


@login_required(login_url='login')
def paciente_alta(request):
    try:
        doctor = Doctor.objects.get(usuario=request.user)
    except Doctor.DoesNotExist:
        doctor = None
        messages.warning(request, "Acceso no autorizado")
        return render(request,
                      'citasmedicas/mensajes_usuarios.html')
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=doctor)
        if form.is_valid():
            clean_data = form.cleaned_data
            nombre = clean_data.get('nombre')
            apellido_paterno = clean_data.get('apellido_paterno')
            apellido_materno = clean_data.get('apellido_materno')
            telefono_personal = clean_data.get('telefono_personal')
            fecha_nacimiento = clean_data.get('fecha_nacimiento')
            email = clean_data.get('email')
            paciente_model = Paciente()
            paciente_model.doctor = doctor
            paciente_model.nombre = nombre
            paciente_model.apellido_paterno = apellido_paterno
            paciente_model.apellido_materno = apellido_materno
            paciente_model.telefono_personal = telefono_personal
            paciente_model.fecha_nacimiento = fecha_nacimiento
            paciente_model.save()
            messages.success(request, 'Paciente guardado con exitó')
            return redirect('paciente_lista')
    else:
        form = PacienteForm()
    return render(request,
                  'citasmedicas/paciente_alta.html',
                  {'form': form})


@login_required(login_url='login')
def paciente_editar(request, pk=0):
    try:
        doctor = Doctor.objects.get(usuario=request.user)
    except Doctor.DoesNotExist:
        doctor = None
        messages.warning(request, "Acceso no autorizado")
        return render(request,
                      'citasmedicas/mensajes_usuarios.html')
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            nombre = clean_data.get('nombre')
            apellido_paterno = clean_data.get('apellido_paterno')
            apellido_materno = clean_data.get('apellido_materno')
            telefono_personal = clean_data.get('telefono_personal')
            fecha_nacimiento = clean_data.get('fecha_nacimiento')
            paciente_model = Paciente(pk)
            paciente_model.doctor = doctor
            paciente_model.nombre = nombre
            paciente_model.apellido_paterno = apellido_paterno
            paciente_model.apellido_materno = apellido_materno
            paciente_model.telefono_personal = telefono_personal
            paciente_model.fecha_nacimiento = fecha_nacimiento
            paciente_model.save()
            messages.success(request, 'Paciente se actualizo con exitó')
            return redirect('paciente_lista')
    else:
        try:
            paciente = Paciente.objects.get(pk=pk)
            form = PacienteForm(instance=paciente)
        except Paciente.DoesNotExist:
            form = None
    return render(request, 'citasmedicas/paciente_alta.html',
                  {'form_edit': form})


@login_required(login_url='login')
def paciente_lista(request):
    try:
        doctor = Doctor.objects.get(usuario=request.user)
    except Doctor.DoesNotExist:
        doctor = None
        messages.warning(request, "Acceso no autorizado")
        return render(request,
                      'citasmedicas/mensajes_usuarios.html')
    results = {}
    query = request.GET.get('q', '')
    if query:
        results['pacientes'] = Paciente.objects.filter(
            Q(doctor=doctor),
            Q(nombre__icontains=query) |
            Q(apellido_materno__icontains=query) |
            Q(apellido_paterno__icontains=query)
        )
        if not results:
            results['pacientes'] = Paciente.objects.filter(doctor=doctor)
    else:
        results['pacientes'] = Paciente.objects.filter(doctor=doctor)
    context = {
        'results': results,
        'query': query
    }
    return render(request, 'citasmedicas/paciente_alta.html', context)


@login_required(login_url='login')
def consultorio_alta(request):
    try:
        doctor = Doctor.objects.get(usuario=request.user)
    except Doctor.DoesNotExist:
        doctor = None
        messages.warning(request, "Acceso no autorizado")
        return render(request,
                      'citasmedicas/mensajes_usuarios.html')
    if request.method == 'POST':
        form = ConsultorioForm(request.POST, instance=doctor)
        if form.is_valid():
            clean_data = form.cleaned_data
            doctor_pk = doctor
            descripcion = clean_data.get('descripcion')
            direccion = clean_data.get('direccion')
            consultorio_model = Consultorio()
            consultorio_model.doctor = doctor_pk
            consultorio_model.descripcion = descripcion
            consultorio_model.direccion = direccion
            consultorio_model.save()
            messages.success(request, 'Consultorio guardado con exitó')
            return redirect('consultorio_lista')
    else:
        form = ConsultorioForm()
    return render(request,
                  'citasmedicas/consultorio_alta.html',
                  {'form': form})


@login_required(login_url='login')
def consultorio_editar(request, pk=0):
    try:
        doctor = Doctor.objects.get(usuario=request.user)
    except Doctor.DoesNotExist:
        doctor = None
        messages.warning(request, "Acceso no autorizado")
        return render(request,
                      'citasmedicas/mensajes_usuarios.html')
    if request.method == 'POST':
        form = ConsultorioForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            direccion = clean_data.get('direccion')
            descripcion = clean_data.get('descripcion')
            consultorio_model = Consultorio(pk)
            consultorio_model.doctor = doctor
            consultorio_model.direccion = direccion
            consultorio_model.descripcion = descripcion
            consultorio_model.save()
            messages.success(request, 'Consultorio se actualizo con exitó')
            return redirect('consultorio_lista')
    else:
        try:
            consultorio = Consultorio.objects.get(pk=pk)
            form = ConsultorioForm(instance=consultorio)
        except Consultorio.DoesNotExist:
            form = None
    return render(request, 'citasmedicas/consultorio_alta.html',
                  {'form_edit': form}
                  )


@login_required(login_url='login')
def consultorio_lista(request):
    try:
        doctor = Doctor.objects.get(usuario=request.user)
    except Doctor.DoesNotExist:
        doctor = None
        messages.warning(request, "Acceso no autorizado")
        return render(request,
                      'citasmedicas/mensajes_usuarios.html')
    results = {}
    query = request.GET.get('q', '')
    if query:
        results['consultorios'] = Consultorio.objects.filter(
            Q(doctor=doctor),
            Q(direccion__icontains=query) |
            Q(descripcion__icontains=query)
        )
        if not results:
            results['consultorios'] = Consultorio.objects.filter(doctor=doctor)
    else:
        results['consultorios'] = Consultorio.objects.filter(doctor=doctor)
    context = {
        'results': results,
        'quer': query
    }
    return render(request, 'citasmedicas/consultorio_alta.html', context)


def lista_doctores_api(request):
    context = {}
    context['doctores'] = Doctor.objects.all()
    html = TemplateResponse(request,
                            'citasmedicas/listadoctores.html', context)
    return HttpResponse(html.render())


class DoctoresViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


@permission_classes((permissions.IsAuthenticated,))
class ListaDoctores(APIView):
    """
    Retrieve, update or delete a doctores instance.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get(self, request, format=None):
        doctores = Doctor.objects.all()
        serializer = DoctorSerializer(doctores, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,))
class DetalleDoctores(APIView):
    """
    Retrieve, update or delete a doctores instance.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get_object(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        doctor = self.get_object(pk)
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
