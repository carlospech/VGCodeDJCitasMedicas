from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
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