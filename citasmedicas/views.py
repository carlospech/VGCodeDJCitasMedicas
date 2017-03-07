# coding: utf-8
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from citasmedicas.forms import LoginForm, SecretariaForm, PacienteForm, ConsultorioForm
from citasmedicas.models import Doctor, Paciente, Consultorio
from django.contrib import messages
from django.core.urlresolvers import reverse



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
                    mensaje = "Usuario logeado"
                else:
                    mensaje = "Usuario inactivo"
            else:
                mensaje = "Usuario o contraseña incorrecto(a)"
    else:
        form = LoginForm()
    return render(request,
                  'citasmedicas/login.html',
                  {'mensaje': mensaje, 'form': form})


def index(request):
    doctores = Doctor.objects.all()
    return render(request,
                  'citasmedicas/index.html',
                  {'doctores': doctores})


def secretaria_alta(request):
    if request.method == "POST":
        form = SecretariaForm(request.POST)
        if form.is_valid():
            secretaria = form.save(commit=False)
            secretaria.doctor = Doctor.objects.get(usuario=request.user)
            secretaria.save()
            return redirect('index')
    else:
        form = SecretariaForm()
    return render(request,
                  'citasmedicas/secretaria_alta.html',
                  {'form': form})

def paciente_alta(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            doctor = clean_data.get('doctor')
            nombre = clean_data.get('nombre')
            apellido_paterno = clean_data.get('apellido_paterno')
            apellido_materno = clean_data.get('apellido_materno')
            telefono_personal = clean_data.get('telefono_personal')
            fecha_nacimiento = clean_data.get('fecha_nacimiento')
            paciente_model = Paciente()
            paciente_model.doctor = doctor
            paciente_model.nombre = nombre
            paciente_model.apellido_paterno = apellido_paterno
            paciente_model.apellido_materno = apellido_materno
            paciente_model.telefono_personal = telefono_personal
            paciente_model.fecha_nacimiento = fecha_nacimiento
            paciente_model.save()
            messages.success(request, 'Paciente guardado con exitó')
            return redirect('paciente_alta')
    else:
        form = PacienteForm()
    pacientes = Paciente.objects.all()
    return render(request,
                  'citasmedicas/paciente_alta.html',
                  {'form':form,
                  'pacientes':pacientes})

def consultorio_alta(request):
    if request.method == 'POST':
        form = ConsultorioForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            doctor = clean_data.get('doctor')
            descripcion = clean_data.get('descripcion')
            direccion = clean_data.get('direccion')
            consultorio_model = Consultorio()
            consultorio_model.doctor = doctor
            consultorio_model.descripcion = descripcion
            consultorio_model.direccion = direccion
            consultorio_model.save()
            messages.success(request, 'Consultorio guardado con exitó')
            return redirect('consultorio_alta')
    else:
        form = ConsultorioForm()
    consultorios = Consultorio.objects.all()
    return render(request,
                  'citasmedicas/consultorio_alta.html',
                  {'form': form,
                   'consultorios': consultorios})