from django.shortcuts import render

from safadordelasdelicias.models import Productos


# Create your views here.

def go_home(request):
    return render(request, 'home.html')

def go_templo(request):
    return render(request, 'templo.html')

def cargar_carta(request):

    lista_productos = Productos.objects.all()

    return render(request, 'carta.html', {'lista_productos': lista_productos})

def go_mesas(request):
    return render(request, 'mesas.html')