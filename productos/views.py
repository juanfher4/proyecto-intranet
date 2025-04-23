from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Cliente, EstadoCliente

@login_required
def productos(request):
    return render(request, 'products/productos.html')

@login_required
def clientes(request, estado_slug):
    estado = None
    estados = EstadoCliente
    clientes = Cliente.objects.all()

    if estado_slug:
        estado = get_object_or_404(EstadoCliente,
                                   slug=estado_slug)
        clientes = clientes.filter(estados=estado)

    return render(request, 'clients/clientes.html', {'clients': clientes,
                                                     'estado': estado,
                                                     'estados': estados})
