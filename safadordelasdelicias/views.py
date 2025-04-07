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

def custom_404(request, exception=None):
    return render(request, '404.html', status=404)
def go_mesa(request):
    return render(request, 'mesa.html')

def go_cocina(request):
    return render(request, 'cocina.html')

def go_carta(request):
    return render(request, 'carta.html')

def go_login(request):
    return render(request, 'login.html')