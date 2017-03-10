from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.citasmedicas_index, name='citasmedicas_index'),
    url(r'^login$', views.login_page, name='login'),
    url(r'^logout$', views.logout_page, name='logout'),
    url(r'^secretaria/alta$', views.secretaria_alta, name='secretaria_alta'),
    url(r'^paciente/alta$', views.paciente_alta, name='paciente_alta'),
    url(r'^consultorio/alta$', views.consultorio_alta, name='consultorio_alta')
]