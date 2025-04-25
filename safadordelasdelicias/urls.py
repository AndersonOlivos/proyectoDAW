from django.conf.urls import handler404
from django.urls import path, re_path

from safadordelasdelicias.views import *

urlpatterns = [
    path('', go_home, name='home'),
    path('home/', go_home , name='home_page'),
    path('templo/', go_templo, name='templo_page'),
    path('carta/', cargar_carta, name='carta'),
    path('mesas/', go_mesas, name='mesas'),
    path('mesas/mesa/<int:id>/',go_mesa, name='mesa'),
    path('mesas/cocina', go_cocina, name='cocina'),
    path('carta/', go_carta, name='carta'),
    path('login/', go_login, name='login'),
    path('admin/', go_admin, name='admin'),
    path('admin/empleados', go_admin, name='admin_empleados'),
    path('admin/carta', go_admin_carta, name='admin_carta'),
    path('admin/contrato', go_admin_contrato, name='admin_contrato'),
    path('tipos_categoria_comidas/', tipos_categoria_comidas, name='tipos_categoria_comidas'),
    path('tipos_subcategorias_comidas/', tipos_subcategorias_comidas, name='tipos_subcategorias_comidas'),
    path('tipos_categoria_tipo_comidas/', tipos_categoria_tipo_comidas, name='tipos_categoria_tipo_comidas'),
    path('enviar_a_cocina/', enviar_a_cocina, name='enviar_a_cocina'),
    path('cargar_historial_pedido/', cargar_historial_pedido, name="cargar_historial_pedido"),

    path('formularioEmpleado/',formularioEmpleados,name='formularioEmpleado'),
]

handler404 = custom_404