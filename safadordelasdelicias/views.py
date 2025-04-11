from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
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
    return render(request, 'mesa.html', {'mesa': mesa})


def go_cocina(request):
    return render(request, 'cocina.html')

def go_carta(request):
    return render(request, 'carta.html')

def go_login(request):
    return render(request, 'login.html')

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
