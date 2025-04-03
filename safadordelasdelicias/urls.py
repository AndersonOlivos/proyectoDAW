from django.conf.urls import handler404
from django.urls import path, re_path

from safadordelasdelicias.views import *

urlpatterns = [
    path('', go_home, name='home'),
    path('home/', go_home , name='home_page'),
    path('templo/', go_templo, name='templo_page'),
    path('carta/', cargar_carta, name='carta'),
    path('mesas/', go_mesas, name='mesas'),
    path('mesas/mesa/',go_mesa, name='mesa'),
]

handler404 = custom_404