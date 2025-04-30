from django.http import JsonResponse, HttpResponse
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

    return render(request, 'mesa.html', {'mesa': mesa, "historial": historial})


def go_cocina(request):

    en_proceso = LineaPedido.objects.filter(estado="En Proceso").exclude(id_producto__categoria=CategoriaProducto.bebida
    ).select_related('id_producto', 'id_pedido')

    pendientes = LineaPedido.objects.filter(estado="Pendiente").exclude(id_producto__categoria=CategoriaProducto.bebida
    ).select_related('id_producto', 'id_pedido')

    lineas_pedidos = list(en_proceso) + list(pendientes)

    datos_pedidos = []
    for linea in lineas_pedidos:
        datos_pedidos.append({
            'id_linea_pedido': linea.id_linea_pedido,
            'nombre_producto': linea.id_producto.nombre,
            'numero_mesa': linea.id_pedido.id_mesa.id,
            'cantidad': linea.cantidad_producto,
            'descripcion': linea.id_producto.descripcion,
            'estado': linea.estado,
        })

    return render(request, 'cocina.html', {'lineas_pedidos': datos_pedidos})


def go_barra(request):

    en_proceso = LineaPedido.objects.filter(estado="En Proceso").exclude(id_producto__categoria=CategoriaProducto.comida
    ).select_related('id_producto', 'id_pedido')

    pendientes = LineaPedido.objects.filter(estado="Pendiente").exclude(id_producto__categoria=CategoriaProducto.comida
    ).select_related('id_producto', 'id_pedido')

    lineas_pedidos = list(en_proceso) + list(pendientes)

    datos_pedidos = []
    for linea in lineas_pedidos:
        datos_pedidos.append({
            'id_linea_pedido': linea.id_linea_pedido,
            'nombre_producto': linea.id_producto.nombre,
            'numero_mesa': linea.id_pedido.id_mesa.id,
            'cantidad': linea.cantidad_producto,
            'descripcion': linea.id_producto.descripcion,
            'estado': linea.estado,
        })

    return render(request, 'barra.html', {'lineas_pedidos': datos_pedidos})
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
                for producto_id, cantidad in productos.items():
                    nueva_linea_pedido = LineaPedido(
                        id_pedido=nuevo_pedido,
                        id_producto=Productos.objects.get(id_Producto=producto_id),
                        cantidad_producto=cantidad,
                        estado=EstadoPedido.pendiente,
                    )
                    nueva_linea_pedido.save()
                    print(f"Nueva linea de pedido para la mesa {mesa_id}")

            elif mesa.estado == "En Curso":
                try:
                    pedido_activo = Pedido.objects.filter(id_mesa=mesa, cerrado=False).first()
                    print(f"Pedido encontrado: {pedido_activo}")

                    for producto_id, cantidad in productos.items():
                        nueva_linea_pedido = LineaPedido(
                            id_pedido=pedido_activo,
                            id_producto=Productos.objects.get(id_Producto=producto_id),
                            cantidad_producto=cantidad,
                            estado=EstadoPedido.pendiente,
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

def cargar_historial_pedido(request):
 id_mesa = request.GET.get('id_mesa')
 if not id_mesa:
     return JsonResponse({'error': 'Parametro id_mesa requerido'}, status=404)

 mesa = get_object_or_404(Mesa, id=id_mesa)
 pedido = Pedido.objects.filter(id_mesa=mesa, cerrado=False).first()
 lineas_pedido = LineaPedido.objects.filter(id_pedido=pedido).select_related('id_producto').all()

 datos_lineas = [
     {
         'producto': linea.id_producto.nombre,
         'cantidad': linea.cantidad_producto,
         'precio_unitario': linea.id_producto.precio,
         'subtotal': linea.cantidad_producto * linea.id_producto.precio,
         'estado': linea.estado,
     }
     for linea in lineas_pedido
 ]

 total = sum(linea['subtotal'] for linea in datos_lineas)

 return JsonResponse({
     'lineas': datos_lineas,
     'total': total
 })

def actualizar_linea_pedido(request):
    id_linea_pedido = request.GET.get('id_linea_pedido')
    estado_linea_pedido = request.GET.get('estado')
    linea_pedido = LineaPedido.objects.get(id_linea_pedido=id_linea_pedido)
    linea_pedido.estado = estado_linea_pedido
    linea_pedido.save()
    return JsonResponse({'status': 'success'})