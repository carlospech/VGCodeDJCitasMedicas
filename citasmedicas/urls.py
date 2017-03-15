from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.citasmedicas_index, name='citasmedicas_index'),
    url(r'^login$', views.login_page, name='login'),
    url(r'^logout$', views.logout_page, name='logout'),
    url(r'^secretaria/alta$', views.secretaria_alta, name='secretaria_alta'),
    url(r'^secretaria/lista$', views.secretaria_lista,
        name='secretaria_lista'),
    url(r'^secretaria/edita/(?P<pk>\d+)$', views.secretaria_edita,
        name='secretaria_edita'),
    url(r'^paciente/alta/$', views.paciente_alta, name='paciente_alta'),
    url(r'^paciente/lista/$', views.paciente_lista, name='paciente_lista'),
    url(r'^paciente/editar/(?P<pk>\d+)/$', views.paciente_editar,
        name='paciente_editar'),
    url(r'^consultorio/alta/$', views.consultorio_alta,
        name='consultorio_alta'),
    url(r'^consultorio/lista/$', views.consultorio_lista,
        name='consultorio_lista'),
    url(r'^consultorio/editar/(?P<pk>\d+)/$', views.consultorio_editar,
        name='consultorio_editar'),
]
