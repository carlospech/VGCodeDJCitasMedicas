from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
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
    mensaje = None
    try:
        doctor = Doctor.objects.get(usuario=request.user)
    except Doctor.DoesNotExist:
        doctor = None
        mensaje = "Acceso no autorizado"
    if request.method == "POST":
        form = SecretariaForm(request.POST)
        if doctor:
            if request.POST['contrasena'] == request.POST['repite_contrasena']:
                if not User.objects.filter(username=request.POST['usuario']).exists():
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
                else:
                    mensaje = "El usuario '" + request.POST['usuario'] + "' ya existe. Capture uno nuevo."
            else:
                mensaje = "La contraseña no es igual, intente de nuevo"
        return render(request,
                      'citasmedicas/secretaria_alta.html',
                      {'mensaje': mensaje, 'form': form})
    else:
        form = SecretariaForm()
    return render(request,
                  'citasmedicas/secretaria_alta.html',
                  {'mensaje': mensaje, 'form': form})