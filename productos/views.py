from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Cliente

@login_required
def productos(request):
    return render(request, 'products/productos.html')

@login_required
def clientes(request):
    clients = Cliente.objects.all()
    return render(request, 'clients/clientes.html', {'clients': clients})
