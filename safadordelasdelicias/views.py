from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import *

from safadordelasdelicias.models import Productos, Mesa


# Create your views here.

def go_home(request):
    return render(request, 'home.html')

def go_templo(request):
    return render(request, 'templo.html')

def cargar_carta(request):

    lista_productos = Productos.objects.all()

    return render(request, 'carta.html', {'lista_productos': lista_productos})

def go_mesas(request):
    lista_mesas = Mesa.objects.all()
    return render(request, 'mesas.html', {'lista_mesas': lista_mesas})


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)

def go_mesa(request, id):
    mesa = get_object_or_404(Mesa, id=id)
    pedido_activo = Pedido.objects.filter(id_mesa=mesa, cerrado=False).first()
    historial = False
    if pedido_activo:
        historial = LineaPedido.objects.filter(id_pedido=pedido_activo).exists()
        lineas_pedido = LineaPedido.objects.filter(id_pedido=pedido_activo)\
                          .select_related('id_producto')\
                          .all()
        total = sum(
            linea.cantidad_producto * linea.id_producto.precio
            for linea in lineas_pedido
        )
        return render(request, 'mesa.html', {'mesa': mesa, "historial": historial, "lineas_pedido": lineas_pedido, "cuenta_total": total})

    return render(request, 'mesa.html', {'mesa': mesa, "historial": historial})


def go_cocina(request):
    return render(request, 'cocina.html')

def go_carta(request):
    return render(request, 'carta.html')

def go_login(request):
    return render(request, 'login.html')

def go_admin(request):
    if request.method == 'POST':
        form = FormularioEmpleado(request.POST)
        if form.is_valid():
            form.save()  # Guarda en la base de datos si es ModelForm
            return redirect('admin')
    else:
        form = FormularioEmpleado()
    return render(request, 'admin.html', {'form': form})

def go_admin_empleados(request):
    return render(request, 'admin.html')

def go_admin_carta(request):
    return render(request, 'admin_carta.html')

def go_admin_contrato(request):
    return render(request, 'admin_contrato.html')

def tipos_categoria_comidas(request):
    categoria = request.GET.get('categoria')
    datos = list(Productos.objects.filter(categoria=categoria).values_list('tipo_categoria', flat=True).distinct())
    return JsonResponse(datos, safe=False)

def tipos_categoria_tipo_comidas(request):
    categoria = request.GET.get('categoria')
    tipo = request.GET.get('tipo')
    subcategoria = request.GET.get('subcategoria')

    if subcategoria == '0':
        datos = list(Productos.objects.filter(categoria=categoria, tipo_categoria=tipo).values())
        return JsonResponse(datos, safe=False)
    else:
        datos = list(Productos.objects.filter(categoria=categoria, tipo_categoria=tipo, subcategoria = subcategoria).values())
        return JsonResponse(datos, safe=False)


def tipos_subcategorias_comidas(request):
    categoria = request.GET.get('categoria')
    tipo = request.GET.get('tipo')
    datos = list(Productos.objects.filter(categoria=categoria, tipo_categoria=tipo).values_list('subcategoria', flat=True).distinct())
    return JsonResponse(datos, safe=False)

def formularioEmpleados(request):
    if request.method == 'POST':
        form = FormularioEmpleado(request.POST)
        if form.is_valid():
            form.save()  # Guarda en la base de datos si es ModelForm
            return redirect('home_page')
    else:
        form = FormularioEmpleado()
    return render(request, 'formularioempleado.html', {'form': form})


def enviar_a_cocina(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Validar que los datos tienen la estructura esperada
            if 'mesa' not in data or 'productos' not in data:
                return JsonResponse({'status': 'error', 'message': 'Formato de datos incorrecto'}, status=400)

            mesa_id = data['mesa']
            productos = data['productos']

            print(f"Pedido para la mesa {mesa_id}:")
            for producto_id, cantidad in productos.items():
                print(f"- Producto {producto_id}: {cantidad} unidades")

            mesa = Mesa.objects.get(id=mesa_id)

            if mesa.estado == "Disponible":
                mesa.estado = "En Curso"
                mesa.save()
                nuevo_pedido = Pedido(id_mesa=mesa, id_empleado=None, cerrado=False)
                nuevo_pedido.save()
                print("PEDIDO CREADO")

            elif mesa.estado == "En Curso":
                try:
                    pedido_activo = Pedido.objects.filter(id_mesa=mesa, cerrado=False).first()
                    print(f"Pedido encontrado: {pedido_activo}")

                    for producto_id, cantidad in productos.items():
                        nueva_linea_pedido = LineaPedido(
                            id_pedido=pedido_activo,
                            id_producto=Productos.objects.get(id_Producto=producto_id),
                            cantidad_producto=cantidad,
                            estado=EstadoPedido.en_proceso,
                        )
                        nueva_linea_pedido.save()
                        print(f"Nueva linea de pedido para la mesa {mesa_id}")

                except Pedido.DoesNotExist:
                    print("No hay pedidos activos para esta mesa")


            return JsonResponse({
                'status': 'success',
                'mesa': mesa_id,
                'productos': productos,
                'message': 'Pedido enviado a cocina correctamente'
            })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Error al decodificar JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)