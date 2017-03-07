from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from citasmedicas.forms import LoginForm, SecretariaForm
from citasmedicas.models import Doctor


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
                    return redirect(request.GET['next'])
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
    return redirect('index')


def index(request):
    doctores = Doctor.objects.all()
    return render(request,
                  'citasmedicas/index.html',
                  {'doctores': doctores})


@login_required(login_url='login')
def secretaria_alta(request):
    mensaje = None
    try:
        doctor = Doctor.objects.get(usuario=request.user)
    except Doctor.DoesNotExist:
        doctor = None
        messages.warning(request, "Acceso no autorizado")
        return render(request,
                      'citasmedicas/mensajes_usuarios.html')
    if request.method == "POST":
        form = SecretariaForm(request.POST)
        if doctor:
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
                return redirect('index')
        return render(request,
                      'citasmedicas/secretaria_alta.html',
                      {'mensaje': mensaje, 'form': form})
    else:
        form = SecretariaForm()
    return render(request,
                  'citasmedicas/secretaria_alta.html',
                  {'mensaje': mensaje, 'form': form})