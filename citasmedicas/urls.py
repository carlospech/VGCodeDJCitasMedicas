from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login_page, name='login'),
    url(r'^secretaria/alta$', views.secretaria_alta, name='alta_secretaria'),
]